from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from . import PlayerInfoId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime
    from .. import UuidColumn


class PlayerInfo(PlayerInfoId):
    """implements `PlayerInfoId`

    id: `uuid`"""

    def __init__(self, uuid: bytes | UuidColumn, latest_username: str, first_join: datetime | DateColumn) -> None:
        super().__init__(uuid)
        self._latest_username = latest_username
        self._first_join = first_join if isinstance(first_join, DateColumn) else DateColumn(first_join)

    class Type(TypedDict):
        uuid: bytes
        latest_username: str
        first_join: datetime

    @property
    def latest_username(self) -> str:
        return self._latest_username

    @property
    def first_join(self) -> DateColumn:
        return self._first_join
