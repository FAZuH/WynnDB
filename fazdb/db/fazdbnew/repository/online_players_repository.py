from __future__ import annotations
from typing import Iterable, TYPE_CHECKING, Any

from . import Repository
from ..model import OnlinePlayers

if TYPE_CHECKING:
    from aiomysql import Connection


class OnlinePlayersRepository(Repository[OnlinePlayers]):

    _TABLE_NAME: str = "online_players"

    async def insert(self, entities: Iterable[OnlinePlayers], conn: None | Connection = None) -> int:
        async with self._db.transaction_group() as tg:
            tg.add(f"DELETE FROM `{self.table_name}` WHERE `uuid` IS NOT NULL")
            tg.add(
                    f"REPLACE INTO `{self.table_name}` (`uuid`, `server`) VALUES (%(uuid)s, %(server)s)",
                    tuple(self._model_to_dict(entity) for entity in entities)
            )
            affected_rows = tg.get_future_affectedrows()
        return affected_rows.result()

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `server` varchar(10) NOT NULL,
                PRIMARY KEY (`uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        await self._db.execute(SQL)

    @staticmethod
    def _model_to_dict(entity: OnlinePlayers) -> dict[str, Any]:
        return {
            "uuid": entity.uuid.uuid,
            "server": entity.server
        }

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
