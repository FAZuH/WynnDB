from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

from . import Repository
from ..model import GuildMemberHistory

if TYPE_CHECKING:
    from aiomysql import Connection


class GuildMemberHistoryRepository(Repository[GuildMemberHistory]):

    _TABLE_NAME: str = "guild_member_history"

    async def insert(self, entities: Iterable[GuildMemberHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}`
                (`uuid`, `contributed`, `joined`, `datetime`, `unique_id`)
            VALUES
                (%(uuid)s, %(contributed)s, %(joined)s, %(datetime)s, %(unique_id)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `contributed` bigint unsigned NOT NULL,
                `joined` datetime NOT NULL,
                `datetime` datetime NOT NULL,
                `unique_id` binary(16) NOT NULL,
                UNIQUE KEY `guildMemberHistory_uq_uniqueId` (`unique_id`),
                KEY `guildMemberHistory_idx_uuidDt` (`uuid`,`datetime` DESC) /*!80000 INVISIBLE */
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
