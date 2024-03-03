from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import CharacterInfo, CharacterInfoId

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans.db import DatabaseQuery
    from kans.util import DbModelDictAdapter, DbModelIdDictAdapter



class CharacterInfoRepository(Repository[CharacterInfo, CharacterInfoId]):

    _TABLE_NAME: str = "character_info"

    def __init__(
        self,
        db: DatabaseQuery,
        db_model_dict_adapter: DbModelDictAdapter,
        db_model_id_dict_adapter: DbModelIdDictAdapter
    ) -> None:
        super().__init__(db)
        self._adapt = db_model_dict_adapter.from_character_info
        self._adapt_id = db_model_id_dict_adapter.from_character_info

    async def insert(self, entities: Iterable[CharacterInfo], conn: None | Connection = None) -> int:
        # NOTE: This doesn't change. Ignore duplicates.
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (`character_uuid`, `uuid`, `type`)
            VALUES (%(character_uuid)s, %(uuid)s, %(type)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def exists(self, id_: CharacterInfoId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `character_uuid` = %(character_uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return result[0].get("COUNT(*)", 0)

    async def find_one(self, id_: CharacterInfoId, conn: None | Connection = None) -> None | CharacterInfo:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `character_uuid` = %(character_uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return CharacterInfo(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> list[CharacterInfo]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [CharacterInfo(**row) for row in result] if result else []

    async def update(self, entities: Iterable[CharacterInfo], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `type` = %(type)s
            WHERE `character_uuid` = %(character_uuid)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: CharacterInfoId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `character_uuid` = %(character_uuid)s"
        return await self._db.execute(SQL, self._adapt_id(id_), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `character_uuid` binary(16) NOT NULL,
                `uuid` binary(16) NOT NULL,
                `type` enum('ARCHER','ASSASSIN','MAGE','SHAMAN','WARRIOR') NOT NULL,
                PRIMARY KEY (`character_uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME