from __future__ import annotations
import asyncio
from datetime import datetime as dt
from typing import TYPE_CHECKING, Generator, Iterable

from .task import Task
from kans.api.wynn.response import GuildResponse, PlayerResponse, OnlinePlayersResponse
from kans.db.model import (
    CharacterHistory,
    CharacterInfo,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    KansUptime,
    OnlinePlayers,
    PlayerActivityHistory,
    PlayerHistory,
    PlayerInfo,
)

if TYPE_CHECKING:
    from datetime import datetime as dt
    from loguru import Logger
    from . import RequestList, ResponseList
    from kans import Api, Database


class TaskDbInsert(Task):
    """Inserts API responses to database."""

    def __init__(
        self,
        logger: Logger,
        api: Api,
        db: Database,
        request_list: RequestList,
        response_list: ResponseList,
    ) -> None:
        self._logger = logger
        self._api = api
        self._db = db
        self._request_list = request_list
        self._response_list = response_list
        self._start_time = dt.now()

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = dt.now()
        self._online_players_manager = _OnlinePlayersManager(api, request_list)
        self._converter = _Converter(self._online_players_manager)
        self._online_guilds_manager = _OnlineGuildsManager(api, self._online_players_manager, request_list)

    def setup(self) -> None:
        self._event_loop.run_until_complete(self._db.create_all())

    def teardown(self) -> None: ...

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())
        self._latest_run = dt.now()

    async def _run(self) -> None:
        await self._db.kans_uptime_repository.insert((KansUptime(self._start_time, dt.now()),))

        player_resps: list[PlayerResponse] = []
        guild_resps: list[GuildResponse] = []
        # NOTE: make sure player response is handled after onlineplayers response.
        # _OnlineGuildManager needs _OnlinePlayersManager.prev_online_uuids to be updated first.
        for resp in self._response_list.get():
            if isinstance(resp, PlayerResponse):
                player_resps.append(resp)
            elif isinstance(resp, OnlinePlayersResponse):
                await self._handle_online_players_response(resp)
            elif isinstance(resp, GuildResponse):
                guild_resps.append(resp)

        if player_resps:
            await self._handle_player_responses(player_resps)
        if guild_resps:
            await self._handle_guild_response(guild_resps)

    async def _handle_online_players_response(self, resp: OnlinePlayersResponse) -> None:
        self._online_players_manager.queue_player_stats(resp)  # Queue logged on players
        self._online_players_manager.requeue_online_players(resp)  # Requeue online players

        # Create DB models
        online_players = tuple(self._converter.to_online_players(resp))
        player_activity_history = tuple(self._converter.to_player_activity_history(resp))

        # Insert to DB
        await self._db.online_players_repository.insert(online_players)
        await self._db.player_activity_history_repository.insert(player_activity_history)

    async def _handle_player_responses(self, resps: list[PlayerResponse]) -> None:
        self._online_guilds_manager.queue_guild_stats(resps)  # Queue logged on guilds

        character_history: list[CharacterHistory] = []
        character_info: list[CharacterInfo] = []
        player_history: list[PlayerHistory] = []
        player_info: list[PlayerInfo] = []
        for resp in resps:
            self._online_players_manager.requeue_player_stats(resp)  # Requeue player stats

            # Create DB models
            character_history.extend(self._converter.to_character_history(resp))
            character_info.extend(self._converter.to_character_info(resp))
            player_history.append(self._converter.to_player_history(resp))
            player_info.append(self._converter.to_player_info(resp))

        # Insert to DB
        await self._db.player_info_repository.insert(player_info)
        await self._db.character_info_repository.insert(character_info)
        await self._db.player_history_repository.insert(player_history)
        await self._db.character_history_repository.insert(character_history)

    async def _handle_guild_response(self, resps: list[GuildResponse]) -> None:
        guild_info = []
        guild_history = []
        guild_member_history = []
        for resp in resps:
            self._online_guilds_manager.requeue_guild_stats(resp)  # Requeue guild stats

            # Create DB models
            guild_info.append(self._converter.to_guild_info(resp))
            guild_history.append(self._converter.to_guild_history(resp))
            guild_member_history.extend(self._converter.to_guild_member_history(resp))

        # Insert to DB
        await self._db.guild_info_repository.insert(guild_info)
        await self._db.guild_history_repository.insert(guild_history)
        await self._db.guild_member_history_repository.insert(guild_member_history)

    @property
    def online_players_manager(self) -> _OnlinePlayersManager:
        return self._online_players_manager

    @property
    def online_guilds_manager(self) -> _OnlineGuildsManager:
        return self._online_guilds_manager

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def latest_run(self) -> dt:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__


class _OnlinePlayersManager:
    """Handles computing new online player responses."""

    def __init__(self, api: Api, request_list: RequestList) -> None:
        self._api = api
        self._request_list = request_list

        self._logged_on: set[str] = set()
        self._logon_timestamps: dict[str, dt] = {}
        self._online_uuids: set[str] = set()

        # Initial request
        self._request_list.put(0, self._api.player.get_online_uuids)

    def queue_player_stats(self, resp: OnlinePlayersResponse) -> None:
        new_online_uuids: set[str] = {str(uuid) for uuid in resp.body.players}
        logged_off: set[str] = self._online_uuids - new_online_uuids
        self._logged_on: set[str] = new_online_uuids - self._online_uuids
        self._online_uuids = new_online_uuids.copy()

        for uuid in logged_off:
            del self._logon_timestamps[uuid]

        for uuid in self._logged_on:
            self._logon_timestamps[uuid] = resp.headers.to_datetime()
            self._request_list.put(0, self._api.player.get_full_stats, uuid)  # Queue new

    def requeue_online_players(self, resp: OnlinePlayersResponse) -> None:
        self._request_list.put(
                resp.headers.expires.to_datetime().timestamp(),
                self._api.player.get_online_uuids,
                priority=0
        )

    def requeue_player_stats(self, resp: PlayerResponse) -> None:
        if resp.body.online is False:
            return

        self._request_list.put(
                resp.headers.expires.to_datetime().timestamp() + 480,  # due to ratelimit
                self._api.player.get_full_stats,
                resp.body.uuid.uuid
        )

    @property
    def logged_on(self) -> set[str]:
        return self._logged_on

    @property
    def logon_timestamps(self) -> dict[str, dt]:
        return self._logon_timestamps

    @property
    def online_uuids(self) -> int:
        return len(self._online_uuids)


class _OnlineGuildsManager:
    """Handles computing new online guild responses."""

    def __init__(self, api: Api, online_players_manager: _OnlinePlayersManager, request_list: RequestList) -> None:
        self._api = api
        self._online_players_manager = online_players_manager
        self._request_list = request_list

        self._online_guilds: dict[str, set[str]] = {}
        """guild_name: set(online_uuids)"""

    def queue_guild_stats(self, resps: Iterable[PlayerResponse]) -> None:
        # NOTE:
        # 1. store dictionaries of guild_names, paired with uuids of online players in that guild
        # 2. if an uuid is online, and not in dictionary, create a new guild entry with the uuid.
        #       this also means that the guild is logged on
        # 3. if an uuid is offline, and in dictionary, remove the uuid from the set of that guild
        # 4. check the guild dictionary, if the set is empty, remove the guild from the dictionary
        #       this also means that the guild is logged off
        logged_off_guilds: set[str] = set()
        logged_on_guilds: set[str] = set()
        for resp in resps:
            if resp.body.guild is None:
                continue

            guild_name = resp.body.guild.name
            is_online = resp.body.online
            uuid = resp.body.uuid.uuid

            if is_online is True and guild_name not in self._online_guilds:
                self._online_guilds[guild_name] = {uuid,}
                logged_on_guilds.add(guild_name)

            if is_online is False and guild_name in self._online_guilds and uuid in self._online_guilds[guild_name]:
                self._online_guilds[guild_name].remove(uuid)

                if len(self._online_guilds[guild_name]) == 0:
                    del self._online_guilds[guild_name]

                logged_off_guilds.add(guild_name)

        for guild_name in logged_on_guilds:
            self._request_list.put(0, self._api.guild.get, guild_name)

    def requeue_guild_stats(self, resp: GuildResponse) -> None:
        if resp.body.members.get_online_members() <= 0:
            return

        self._request_list.put(
                resp.headers.expires.to_datetime().timestamp(),
                self._api.guild.get,
                resp.body.name
        )

    @property
    def online_guilds(self) -> int:
        return len(self._online_guilds)


class _Converter:
    """Converts wynncraft API responses to DB models."""

    def __init__(self, online_players_manager: _OnlinePlayersManager) -> None:
        self._online_players_manager = online_players_manager

    def to_character_history(self, resp: PlayerResponse) -> Generator[CharacterHistory, None, None]:
        return (CharacterHistory(
                character_uuid=ch_uuid.to_bytes(),
                level=ch.level,
                xp=ch.xp,
                wars=ch.wars,
                playtime=ch.playtime,
                mobs_killed=ch.mobs_killed,
                chests_found=ch.chests_found,
                logins=ch.logins,
                deaths=ch.deaths,
                discoveries=ch.discoveries,
                gamemode=ch.gamemode.to_bytes(),
                alchemism=ch.professions.alchemism.to_decimal(),
                armouring=ch.professions.armouring.to_decimal(),
                cooking=ch.professions.cooking.to_decimal(),
                jeweling=ch.professions.jeweling.to_decimal(),
                scribing=ch.professions.scribing.to_decimal(),
                tailoring=ch.professions.tailoring.to_decimal(),
                weaponsmithing=ch.professions.weaponsmithing.to_decimal(),
                woodworking=ch.professions.woodworking.to_decimal(),
                mining=ch.professions.mining.to_decimal(),
                woodcutting=ch.professions.woodcutting.to_decimal(),
                farming=ch.professions.farming.to_decimal(),
                fishing=ch.professions.fishing.to_decimal(),
                dungeon_completions=ch.dungeons.total,
                quest_completions=len(ch.quests),
                raid_completions=ch.raids.total,
                datetime=resp.headers.to_datetime()
        ) for ch_uuid, ch in resp.body.iter_characters())

    def to_character_info(self, resp: PlayerResponse) -> Generator[CharacterInfo, None, None]:
        return (CharacterInfo(
                character_uuid=character_uuid.to_bytes(),
                uuid=resp.body.uuid.to_bytes(),
                type=character.type.get_kind()
        ) for character_uuid, character in resp.body.iter_characters())

    def to_guild_history(self, resp: GuildResponse) -> GuildHistory:
        return GuildHistory(
                name=resp.body.name,
                level=resp.body.level,
                territories=resp.body.territories,
                wars=resp.body.wars,
                member_total=resp.body.members.total,
                online_members=resp.body.members.get_online_members(),
                datetime=resp.headers.to_datetime()
        )

    def to_guild_info(self, resp: GuildResponse) -> GuildInfo:
        return GuildInfo(
                name=resp.body.name,
                prefix=resp.body.prefix,
                created=resp.body.created.to_datetime()
        )

    def to_guild_member_history(self, resp: GuildResponse) -> Generator[GuildMemberHistory, None, None]:
        return (GuildMemberHistory(
                uuid=uuid.to_bytes() if uuid.is_uuid() else memberinfo.uuid.to_bytes(),  # type: ignore
                contributed=memberinfo.contributed,
                joined=memberinfo.joined.to_datetime(),
                datetime=resp.headers.to_datetime()
        ) for rank, uuid, memberinfo in resp.body.members.iter_online_members())  # type: ignore

    def to_online_players(self, resp: OnlinePlayersResponse) -> Generator[OnlinePlayers, None, None]:
        return (OnlinePlayers(uuid=uuid.to_bytes(), server=server) for uuid, server in resp.body.iter_players())

    def to_player_activity_history(self, resp: OnlinePlayersResponse) -> Generator[PlayerActivityHistory, None, None]:
        return (PlayerActivityHistory(
                        uuid.username_or_uuid,
                        self._online_players_manager.logon_timestamps[uuid.username_or_uuid],
                        resp.headers.to_datetime()
                )
                for uuid in resp.body.players
                if (uuid.is_uuid() and uuid.username_or_uuid in self._online_players_manager.logged_on)
        )

    def to_player_history(self, resp: PlayerResponse) -> PlayerHistory:
        return PlayerHistory(
                uuid=resp.body.uuid.to_bytes(),
                username=resp.body.username,
                support_rank=resp.body.support_rank,
                playtime=resp.body.playtime,
                guild_name=resp.body.guild.name if resp.body.guild else None,
                guild_rank=resp.body.guild.rank if resp.body.guild else None,
                rank=resp.body.rank,
                datetime=resp.headers.to_datetime()
        )

    def to_player_info(self, resp: PlayerResponse) -> PlayerInfo:
        return PlayerInfo(
                uuid=resp.body.uuid.to_bytes(),
                latest_username=resp.body.username,
                first_join=resp.body.first_join.to_datetime()
        )