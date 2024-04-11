from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import GuildHistory

if TYPE_CHECKING:
    from aiomysql import Connection


class GuildHistoryRepository(Repository[GuildHistory]):

    _TABLE_NAME: str = "guild_history"

    async def insert(self, entities: Iterable[GuildHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}`
                (`name`, `level`, `territories`, `wars`, `member_total`, `online_members`, `datetime`, `unique_id`)
            VALUES
                (%(name)s, %(level)s, %(territories)s, %(wars)s, %(member_total)s, %(online_members)s, %(datetime)s, %(unique_id)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `name` varchar(30) NOT NULL,
                `level` decimal(5,2) unsigned NOT NULL,
                `territories` smallint unsigned NOT NULL,
                `wars` int unsigned NOT NULL,
                `member_total` tinyint unsigned NOT NULL,
                `online_members` tinyint unsigned NOT NULL,
                `datetime` datetime NOT NULL,
                `unique_id` binary(16) NOT NULL,
                UNIQUE KEY `guildHistory_uq_uniqueId` (`unique_id`),
                KEY `guildHistory_idx_nameDt` (`name`,`datetime` DESC) /*!80000 INVISIBLE */
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)
    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
