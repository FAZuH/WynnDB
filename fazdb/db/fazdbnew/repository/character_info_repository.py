from __future__ import annotations
from typing import Any, Iterable, TYPE_CHECKING

from . import Repository
from ..model import CharacterInfo

if TYPE_CHECKING:
    from aiomysql import Connection


class CharacterInfoRepository(Repository[CharacterInfo]):

    _TABLE_NAME: str = "character_info"

    async def insert(self, entities: Iterable[CharacterInfo], conn: None | Connection = None) -> int:
        # NOTE: This doesn't change. Ignore duplicates.
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (`character_uuid`, `uuid`, `type`)
            VALUES (%(character_uuid)s, %(uuid)s, %(type)s)
        """
        return await self._db.execute_many(SQL, tuple(self._model_to_dict(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `character_uuid` binary(16) NOT NULL,
                `uuid` binary(16) NOT NULL,
                `type` enum('ARCHER','ASSASSIN','MAGE','SHAMAN','WARRIOR') NOT NULL,
                PRIMARY KEY (`character_uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        await self._db.execute(SQL)

    @staticmethod
    def _model_to_dict(entity: CharacterInfo) -> dict[str, Any]:
        return {
            "character_uuid": entity.character_uuid.uuid,
            "uuid": entity.uuid.uuid,
            "type": entity.type
        }

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
