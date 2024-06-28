from __future__ import annotations
from typing import Any, Iterable, TYPE_CHECKING

from . import Repository
from ..model import PlayerInfo

if TYPE_CHECKING:
    from aiomysql import Connection


class PlayerInfoRepository(Repository[PlayerInfo]):

    _TABLE_NAME: str = "player_info"

    async def insert(self, entities: Iterable[PlayerInfo], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`uuid`, `latest_username`, `first_join`)
            VALUES (%(uuid)s, %(latest_username)s, %(first_join)s)
        """
        return await self._db.execute_many(SQL, tuple(self._model_to_dict(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `latest_username` varchar(16) NOT NULL,
                `first_join` datetime NOT NULL,
                PRIMARY KEY (`uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        await self._db.execute(SQL)

    @staticmethod
    def _model_to_dict(entity: PlayerInfo) -> dict[str, Any]:
        return {
            "uuid": entity.uuid.uuid,
            "latest_username": entity.latest_username,
            "first_join": entity.first_join.datetime
        }

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
