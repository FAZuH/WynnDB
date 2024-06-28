from __future__ import annotations
from typing import Any, Iterable, TYPE_CHECKING

from . import Repository
from ..model import PlayerActivityHistory

if TYPE_CHECKING:
    from aiomysql import Connection


class PlayerActivityHistoryRepository(Repository[PlayerActivityHistory]):

    _TABLE_NAME: str = "player_activity_history"

    async def insert(self, entities: Iterable[PlayerActivityHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`uuid`, `logon_datetime`, `logoff_datetime`)
            VALUES (%(uuid)s, %(logon_datetime)s, %(logoff_datetime)s)
        """
        return await self._db.execute_many(SQL, tuple(self._model_to_dict(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `logon_datetime` datetime NOT NULL,
                `logoff_datetime` datetime NOT NULL,
                UNIQUE KEY `player_uptime_uq_uuidlogon` (`uuid`,`logon_datetime`),
                KEY `player_uptime_idx_logon_timestamp` (`logon_datetime` DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        await self._db.execute(SQL)

    @staticmethod
    def _model_to_dict(entity: PlayerActivityHistory) -> dict[str, Any]:
        return {
            "uuid": entity.uuid.uuid,
            "logon_datetime": entity.logon_datetime.datetime,
            "logoff_datetime": entity.logoff_datetime.datetime,
        }

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
