from __future__ import annotations
from typing import Any, Iterable, TYPE_CHECKING

from . import Repository
from ..model import CharacterHistory

if TYPE_CHECKING:
    from aiomysql import Connection


class CharacterHistoryRepository(Repository[CharacterHistory]):

    _TABLE_NAME: str = "character_history"

    async def insert(self, entities: Iterable[CharacterHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (
                `character_uuid`, `level`, `xp`, `wars`, `playtime`, `mobs_killed`, `chests_found`, `logins`,
                `deaths`, `discoveries`, `hardcore`, `ultimate_ironman`, `ironman`, `craftsman`, `hunted`,
                `alchemism`, `armouring`, `cooking`, `jeweling`, `scribing`, `tailoring`, `weaponsmithing`,
                `woodworking`, `mining`, `woodcutting`, `farming`, `fishing`, `dungeon_completions`, 
                `quest_completions`, `raid_completions`, `datetime`, `unique_id`
            )
            VALUES (
                %(character_uuid)s, %(level)s, %(xp)s, %(wars)s, %(playtime)s, %(mobs_killed)s, %(chests_found)s, %(logins)s,
                %(deaths)s, %(discoveries)s, %(hardcore)s, %(ultimate_ironman)s, %(ironman)s, %(craftsman)s, %(hunted)s,
                %(alchemism)s, %(armouring)s, %(cooking)s, %(jeweling)s, %(scribing)s, %(tailoring)s, %(weaponsmithing)s,
                %(woodworking)s, %(mining)s, %(woodcutting)s, %(farming)s, %(fishing)s, %(dungeon_completions)s, 
                %(quest_completions)s, %(raid_completions)s, %(datetime)s, %(unique_id)s
            )
        """
        return await self._db.execute_many(SQL, tuple(self._model_to_dict(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `character_uuid` binary(16) NOT NULL,
                `level` tinyint unsigned NOT NULL,
                `xp` bigint unsigned NOT NULL,
                `wars` int unsigned NOT NULL,
                `playtime` decimal(7,2) unsigned NOT NULL,
                `mobs_killed` int unsigned NOT NULL,
                `chests_found` int unsigned NOT NULL,
                `logins` int unsigned NOT NULL,
                `deaths` int unsigned NOT NULL,
                `discoveries` int unsigned NOT NULL,
                `hardcore` boolean NOT NULL,
                `ultimate_ironman` boolean NOT NULL,
                `ironman` boolean NOT NULL,
                `craftsman` boolean NOT NULL,
                `hunted` boolean NOT NULL,
                `alchemism` decimal(5,2) unsigned NOT NULL,
                `armouring` decimal(5,2) unsigned NOT NULL,
                `cooking` decimal(5,2) unsigned NOT NULL,
                `jeweling` decimal(5,2) unsigned NOT NULL,
                `scribing` decimal(5,2) unsigned NOT NULL,
                `tailoring` decimal(5,2) unsigned NOT NULL,
                `weaponsmithing` decimal(5,2) unsigned NOT NULL,
                `woodworking` decimal(5,2) unsigned NOT NULL,
                `mining` decimal(5,2) unsigned NOT NULL,
                `woodcutting` decimal(5,2) unsigned NOT NULL,
                `farming` decimal(5,2) unsigned NOT NULL,
                `fishing` decimal(5,2) unsigned NOT NULL,
                `dungeon_completions` int unsigned NOT NULL,
                `quest_completions` int unsigned NOT NULL,
                `raid_completions` int unsigned NOT NULL,
                `datetime` datetime NOT NULL,
                `unique_id` binary(16) NOT NULL,
                UNIQUE KEY `characterHistory_uq_uniqueId` (`unique_id`),
                KEY `characterHistory_idx_chuuidDt` (`character_uuid`,`datetime` DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        await self._db.execute(SQL, connection=conn)

    @staticmethod
    def _model_to_dict(entity: CharacterHistory) -> dict[str, Any]:
        return {
            "character_uuid": entity.character_uuid.uuid,
            "level": entity.level,
            "xp": entity.xp,
            "wars": entity.wars,
            "playtime": entity.playtime,
            "mobs_killed": entity.mobs_killed,
            "chests_found": entity.chests_found,
            "logins": entity.logins,
            "deaths": entity.deaths,
            "discoveries": entity.discoveries,
            "alchemism": entity.alchemism,
            "hardcore": entity.hardcore,
            "ultimate_ironman": entity.ultimate_ironman,
            "ironman": entity.ironman,
            "craftsman": entity.craftsman,
            "hunted": entity.hunted,
            "armouring": entity.armouring,
            "cooking": entity.cooking,
            "jeweling": entity.jeweling,
            "scribing": entity.scribing,
            "tailoring": entity.tailoring,
            "weaponsmithing": entity.weaponsmithing,
            "woodworking": entity.woodworking,
            "mining": entity.mining,
            "woodcutting": entity.woodcutting,
            "farming": entity.farming,
            "fishing": entity.fishing,
            "dungeon_completions": entity.dungeon_completions,
            "quest_completions": entity.quest_completions,
            "raid_completions": entity.raid_completions,
            "datetime": entity.datetime.datetime,
            "unique_id": entity.unique_id.uuid
        }

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
