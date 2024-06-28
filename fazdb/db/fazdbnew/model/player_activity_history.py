from __future__ import annotations
from typing import TYPE_CHECKING

from .column import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class PlayerActivityHistory:

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        logon_datetime: datetime | DateColumn,
        logoff_datetime: datetime | DateColumn,
    ) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._logon_datetime = logon_datetime if isinstance(logon_datetime, DateColumn) else DateColumn(logon_datetime)
        self._logoff_datetime = logoff_datetime if isinstance(logoff_datetime, DateColumn) else DateColumn(logoff_datetime)

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def logon_datetime(self) -> DateColumn:
        return self._logon_datetime

    @property
    def logoff_datetime(self) -> DateColumn:
        return self._logoff_datetime
