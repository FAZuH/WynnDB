from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from .. import UuidColumn, DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildMemberHistoryId:

    def __init__(self, uuid: bytes | UuidColumn, datetime: datetime | DateColumn) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    class IdType(TypedDict):
        uuid: bytes
        datetime: datetime

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime