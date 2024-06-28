from __future__ import annotations
from typing import TYPE_CHECKING

from .column import DateColumn, UniqueIdMixin, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildMemberHistory(UniqueIdMixin):

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        contributed: int,
        joined: datetime | DateColumn,
        datetime: datetime | DateColumn,
        unique_id: bytes | UuidColumn | None = None
    ) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)
        self._contributed = contributed
        self._joined = joined if isinstance(joined, DateColumn) else DateColumn(joined)

        super().__init__(unique_id, uuid, contributed, joined)

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime

    @property
    def contributed(self) -> int:
        return self._contributed

    @property
    def joined(self) -> DateColumn:
        return self._joined
