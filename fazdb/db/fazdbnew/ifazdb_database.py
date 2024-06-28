from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from decimal import Decimal
    from .. import DatabaseQuery
    from .repository import (
        CharacterInfoRepository,
        CharacterHistoryRepository,
        GuildInfoRepository,
        GuildHistoryRepository,
        GuildMemberHistoryRepository,
        FazDbUptimeRepository,
        OnlinePlayersRepository,
        PlayerActivityHistoryRepository,
        PlayerInfoRepository,
        PlayerHistoryRepository,
    )


class IFazDbDatabase(Protocol):
    """<<interface>>

    implemented by `WynndataDatabase`"""
    async def create_all(self) -> None: ...
    async def total_size(self) -> Decimal: ...
    @property
    def character_history_repository(self) -> CharacterHistoryRepository: ...
    @property
    def character_info_repository(self) -> CharacterInfoRepository: ...
    @property
    def guild_history_repository(self) -> GuildHistoryRepository: ...
    @property
    def guild_info_repository(self) -> GuildInfoRepository: ...
    @property
    def guild_member_history_repository(self) -> GuildMemberHistoryRepository: ...
    @property
    def fazdb_uptime_repository(self) -> FazDbUptimeRepository: ...
    @property
    def online_players_repository(self) -> OnlinePlayersRepository: ...
    @property
    def player_activity_history_repository(self) -> PlayerActivityHistoryRepository: ...
    @property
    def player_history_repository(self) -> PlayerHistoryRepository: ...
    @property
    def player_info_repository(self) -> PlayerInfoRepository: ...
    @property
    def query(self) -> DatabaseQuery: ...
