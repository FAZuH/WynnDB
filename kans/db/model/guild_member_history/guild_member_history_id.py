from __future__ import annotations
from typing import TYPE_CHECKING

from .. import UuidColumn, DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class GuildMemberHistoryId:

    def __init__(self, uuid: bytes | UuidColumn, datetime: dt | DateColumn) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
