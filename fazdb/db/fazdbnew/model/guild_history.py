from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING

from .column import DateColumn, UniqueIdMixin, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildHistory(UniqueIdMixin):

    def __init__(
        self,
        name: str,
        level: Decimal,
        territories: int,
        wars: int,
        member_total: int,
        online_members: int,
        datetime: datetime | DateColumn,
        unique_id: bytes | UuidColumn | None = None
    ) -> None:
        self._name = name
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)
        self._level = level
        self._territories = territories
        self._wars = wars
        self._member_total = member_total
        self._online_members = online_members

        super().__init__(unique_id, name, level, territories, wars, member_total, online_members)

    @property
    def name(self) -> str:
        return self._name

    @property
    def datetime(self) -> DateColumn:
        return self._datetime

    @property
    def level(self) -> Decimal:
        return self._level

    @property
    def territories(self) -> int:
        return self._territories

    @property
    def wars(self) -> int:
        return self._wars

    @property
    def member_total(self) -> int:
        return self._member_total

    @property
    def online_members(self) -> int:
        return self._online_members
