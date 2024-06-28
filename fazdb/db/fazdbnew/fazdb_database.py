from __future__ import annotations
from decimal import Decimal
from typing import Any, TYPE_CHECKING

from . import IFazDbDatabase
from .repository import (
    CharacterHistoryRepository,
    CharacterInfoRepository,
    GuildHistoryRepository,
    GuildInfoRepository,
    GuildMemberHistoryRepository,
    OnlinePlayersRepository,
    PlayerActivityHistoryRepository,
    PlayerHistoryRepository,
    PlayerInfoRepository,
    Repository,
    FazDbUptimeRepository,
)

if TYPE_CHECKING:
    from .. import DatabaseQuery
    from fazdb import Logger


class FazDbDatabase(IFazDbDatabase):

    def __init__(self, logger: Logger, database_query: DatabaseQuery) -> None:
        self._logger = logger
        self._dbquery = database_query

        self._character_history_repository = CharacterHistoryRepository(self.query)
        self._character_info_repository = CharacterInfoRepository(self.query)
        self._guild_history_repository = GuildHistoryRepository(self.query)
        self._guild_info_repository = GuildInfoRepository(self.query)
        self._guild_member_history_repository = GuildMemberHistoryRepository(self.query)
        self._fazdb_uptime_repository = FazDbUptimeRepository(self.query)
        self._online_players_repository = OnlinePlayersRepository(self.query)
        self._player_activity_history_repository = PlayerActivityHistoryRepository(self.query)
        self._player_history_repository = PlayerHistoryRepository(self.query)
        self._player_info_repository = PlayerInfoRepository(self.query)
        self._repositories: list[Repository[Any]] = [
                self._character_history_repository,
                self._character_info_repository,
                self._guild_history_repository,
                self._guild_info_repository,
                self._guild_member_history_repository,
                self._fazdb_uptime_repository,
                self._online_players_repository,
                self._player_activity_history_repository,
                self._player_history_repository,
                self._player_info_repository,
        ]

    async def create_all(self) -> None:
        for repo in self._repositories:
            await repo.create_table()

    async def total_size(self) -> Decimal:
        sum_size = Decimal(0)
        for repo in self._repositories:
            sum_size += await repo.table_size()
        return sum_size

    @property
    def guild_history_repository(self) -> GuildHistoryRepository:
        return self._guild_history_repository

    @property
    def guild_info_repository(self) -> GuildInfoRepository:
        return self._guild_info_repository

    @property
    def guild_member_history_repository(self) -> GuildMemberHistoryRepository:
        return self._guild_member_history_repository

    @property
    def fazdb_uptime_repository(self) -> FazDbUptimeRepository:
        return self._fazdb_uptime_repository

    @property
    def player_activity_history_repository(self) -> PlayerActivityHistoryRepository:
        return self._player_activity_history_repository

    @property
    def character_history_repository(self) -> CharacterHistoryRepository:
        return self._character_history_repository

    @property
    def character_info_repository(self) -> CharacterInfoRepository:
        return self._character_info_repository

    @property
    def player_history_repository(self) -> PlayerHistoryRepository:
        return self._player_history_repository

    @property
    def player_info_repository(self) -> PlayerInfoRepository:
        return self._player_info_repository

    @property
    def online_players_repository(self) -> OnlinePlayersRepository:
        return self._online_players_repository

    @property
    def query(self) -> DatabaseQuery:
        return self._dbquery
