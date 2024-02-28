from __future__ import annotations
from typing import TYPE_CHECKING, Generator

from kans.db.model import (
    CharacterHistory,
    CharacterInfo,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    OnlinePlayers,
    PlayerActivityHistory,
    PlayerHistory,
    PlayerInfo
)

if TYPE_CHECKING:
    from datetime import datetime
    from kans.api.wynn.response import GuildResponse, OnlinePlayersResponse, PlayerResponse



class ApiToDbConverter:
    """Converts wynncraft API responses to DB models."""
    @staticmethod
    def to_character_history(resp: PlayerResponse) -> Generator[CharacterHistory, None, None]:
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
                gamemode=ch.gamemode.get_liststr(),
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

    @staticmethod
    def to_character_info(resp: PlayerResponse) -> Generator[CharacterInfo, None, None]:
        return (CharacterInfo(
                character_uuid=character_uuid.to_bytes(),
                uuid=resp.body.uuid.to_bytes(),
                type=character.type.get_kind_str()
        ) for character_uuid, character in resp.body.iter_characters())

    @staticmethod
    def to_guild_history(resp: GuildResponse) -> GuildHistory:
        return GuildHistory(
                name=resp.body.name,
                level=resp.body.level,
                territories=resp.body.territories,
                wars=resp.body.wars,
                member_total=resp.body.members.total,
                online_members=resp.body.members.get_online_members(),
                datetime=resp.headers.to_datetime()
        )

    @staticmethod
    def to_guild_info(resp: GuildResponse) -> GuildInfo:
        return GuildInfo(
                name=resp.body.name,
                prefix=resp.body.prefix,
                created=resp.body.created.to_datetime()
        )

    @staticmethod
    def to_guild_member_history(resp: GuildResponse) -> Generator[GuildMemberHistory, None, None]:
        return (GuildMemberHistory(
                uuid=uuid.to_bytes() if uuid.is_uuid() else memberinfo.uuid.to_bytes(),  # type: ignore
                contributed=memberinfo.contributed,
                joined=memberinfo.joined.to_datetime(),
                datetime=resp.headers.to_datetime()
        ) for rank, uuid, memberinfo in resp.body.members.iter_online_members())  # type: ignore

    @staticmethod
    def to_online_players(resp: OnlinePlayersResponse) -> Generator[OnlinePlayers, None, None]:
        return (OnlinePlayers(uuid=uuid.to_bytes(), server=server) for uuid, server in resp.body.iter_players())

    @staticmethod
    def to_player_activity_history(
        resp: OnlinePlayersResponse,
        logged_on: set[str],
        logon_timestamps: dict[str, datetime]
    ) -> Generator[PlayerActivityHistory, None, None]:
        return (PlayerActivityHistory(
                        uuid.username_or_uuid,
                        logon_timestamps[uuid.username_or_uuid],
                        resp.headers.to_datetime()
                )
                for uuid in resp.body.players
                if (uuid.is_uuid() and uuid.username_or_uuid in logged_on)
        )

    @staticmethod
    def to_player_history(resp: PlayerResponse) -> PlayerHistory:
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

    @staticmethod
    def to_player_info(resp: PlayerResponse) -> PlayerInfo:
        return PlayerInfo(
                uuid=resp.body.uuid.to_bytes(),
                latest_username=resp.body.username,
                first_join=resp.body.first_join.to_datetime()
        )