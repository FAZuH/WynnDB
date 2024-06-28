from __future__ import annotations
from typing import TYPE_CHECKING

from .column import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class PlayerInfo:

    def __init__(self, uuid: bytes | UuidColumn, latest_username: str, first_join: datetime | DateColumn) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._latest_username = latest_username
        self._first_join = first_join if isinstance(first_join, DateColumn) else DateColumn(first_join)

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def latest_username(self) -> str:
        return self._latest_username

    @property
    def first_join(self) -> DateColumn:
        return self._first_join
