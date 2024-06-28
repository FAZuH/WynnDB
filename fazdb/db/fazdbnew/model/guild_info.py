from __future__ import annotations
from typing import TYPE_CHECKING

from .column import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildInfo:

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        name: str,
        prefix: str,
        created: datetime | DateColumn
    ) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._name = name
        self._prefix = prefix
        self._created = created if isinstance(created, DateColumn) else DateColumn(created)

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def name(self) -> str:
        return self._name

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def created(self) -> DateColumn:
        return self._created
