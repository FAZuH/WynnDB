from __future__ import annotations
from typing import Any, Iterable, TYPE_CHECKING

from . import Repository
from ..model import FazDbUptime

if TYPE_CHECKING:
    from aiomysql import Connection


class FazDbUptimeRepository(Repository[FazDbUptime]):

    _TABLE_NAME: str = "kans_uptime"

    async def insert(self, entities: Iterable[FazDbUptime], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`start_time`, `stop_time`)
            VALUES (%(start_time)s, %(stop_time)s)
        """
        return await self._db.execute_many(SQL, tuple(self._model_to_dict(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `start_time` datetime NOT NULL,
                `stop_time` datetime NOT NULL,
                PRIMARY KEY (`start_time`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        await self._db.execute(SQL, connection=conn)

    @staticmethod
    def _model_to_dict(entity: FazDbUptime) -> dict[str, Any]:
        return {
            "start_time": entity.start_time.datetime,
            "stop_time": entity.stop_time.datetime
        }

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
