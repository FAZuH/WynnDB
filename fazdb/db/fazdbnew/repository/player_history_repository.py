from __future__ import annotations
from typing import Any, Iterable, TYPE_CHECKING

from . import Repository
from ..model import PlayerHistory

if TYPE_CHECKING:
    from aiomysql import Connection


class PlayerHistoryRepository(Repository[PlayerHistory]):

    _TABLE_NAME: str = "player_history"

    async def insert(self, entities: Iterable[PlayerHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}`
                (`uuid`, `username`, `support_rank`, `playtime`, `guild_name`, `guild_rank`, `rank`, `datetime`, `unique_id`)
            VALUES
                (%(uuid)s, %(username)s, %(support_rank)s, %(playtime)s, %(guild_name)s, %(guild_rank)s, %(rank)s, %(datetime)s, %(unique_id)s)
        """
        return await self._db.execute_many(SQL, tuple(self._model_to_dict(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `username` varchar(16) NOT NULL,
                `support_rank` varchar(45) DEFAULT NULL,
                `playtime` decimal(8,2) unsigned NOT NULL,
                `guild_name` varchar(30) DEFAULT NULL,
                `guild_rank` enum('OWNER','CHIEF','STRATEGIST','CAPTAIN','RECRUITER','RECRUIT') DEFAULT NULL,
                `rank` varchar(30) DEFAULT NULL,
                `datetime` datetime NOT NULL,
                `unique_id` binary(16) NOT NULL,
                UNIQUE KEY `playerHistory_uq_uniqueId` (`unique_id`),
                KEY `playerHistory_idx_uuidDt` (`uuid`,`datetime` DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        await self._db.execute(SQL)

    @staticmethod
    def _model_to_dict(entity: PlayerHistory) -> dict[str, Any]:
        return {
            "uuid": entity.uuid.uuid,
            "username": entity.username,
            "support_rank": entity.support_rank,
            "playtime": entity.playtime,
            "guild_name": entity.guild_name,
            "guild_rank": entity.guild_rank,
            "rank": entity.rank,
            "datetime": entity.datetime.datetime,
            "unique_id": entity.unique_id.uuid
        }

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
