from __future__ import annotations
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from uuid import UUID
    from kans import GuildResponse, PlayerResponse, PlayersResponse


class Api(Protocol):
    async def start(self) -> None: ...
    async def close(self) -> None: ...
    async def get_guild_stats(self, name_or_prefix: str, is_prefix: bool = False) -> GuildResponse: ...
    async def get_online_uuids(self) -> PlayersResponse: ...
    async def get_player_stats(self, username_or_uuid: str | UUID) -> PlayerResponse: ...
    async def __aenter__(self) -> Api: ...
    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any): ...
