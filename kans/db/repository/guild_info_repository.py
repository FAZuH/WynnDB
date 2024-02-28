from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import GuildInfo, GuildInfoId

if TYPE_CHECKING:
    from aiomysql import Connection


class GuildInfoRepository(Repository[GuildInfo, GuildInfoId]):

    _TABLE_NAME = "guild_info"

    async def insert(self, entities: Iterable[GuildInfo], conn: None | Connection = None) -> int:
        # NOTE: This doesn't change. Ignore duplicates.
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (`name`, `prefix`, `created`)
            VALUES (%(name)s, %(prefix)s, %(created)s)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_dict() for entity in entities), conn)

    async def exists(self, id_: GuildInfoId, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: GuildInfoId, conn: None | Connection = None) -> None | GuildInfo: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[GuildInfo]: ...

    async def update(self, entities: Iterable[GuildInfo], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: GuildInfoId, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `name` varchar(30) NOT NULL,
                `prefix` varchar(4) NOT NULL,
                `created` datetime NOT NULL,
                PRIMARY KEY (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
