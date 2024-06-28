from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


class DateColumn:

    _MYSQL_DT_FMT: str = "%Y-%m-%d %H:%M:%S"

    def __init__(self, datetime: datetime):
        self._datetime = datetime

    def to_sqldt(self) -> str:
        return self._datetime.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def mysql_dt_fmt(self) -> str:
        return self._MYSQL_DT_FMT
