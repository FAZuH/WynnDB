# pyright: reportPrivateUsage=none
import unittest
from uuid import UUID

from wynndb.config import Config
from wynndb.db import WynnDbDatabase
from wynndb.db.wynndb.model import OnlinePlayers
from wynndb.logger.wynndb_logger import WynnDbLogger
from wynndb.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestOnlinePlayersRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        Config.load_config()
        self._adapter = ApiResponseAdapter()
        self._db = WynnDbDatabase(WynnDbLogger())
        self._repo = self._db.online_players_repository

        self._repo._TABLE_NAME = "test_online_players"
        await self._repo.create_table()

        self._testData = self._get_data()

    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        # NOTE: Assert if the table exists
        res = await self._repo._db.fetch(f"SHOW TABLES LIKE '{self._repo._TABLE_NAME}'")
        self.assertEqual(self._repo.table_name, next(iter(res[0].values())))

    async def test_insert(self) -> None:
        # ACT
        n = await self._repo.insert(self._testData)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        self.assertEqual(10, n)

        # PREPARE
        toTest1: list[OnlinePlayers] = []
        for i, e in enumerate(self._testData):
            as_dict = self._repo._adapt(e)
            as_dict["uuid"] = UUID(int=69 + i).bytes
            toTest1.append(e.__class__(**as_dict))

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints.
        # self.assertEqual(len(toTest1), (await self._repo.count()))  # TODO:

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return

    def _get_data(self) -> list[OnlinePlayers]:
        fixtures = FixturesApi()
        raw_test_data = list(self._adapter.OnlinePlayers.to_online_players(fixtures.get_online_uuids()))
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEqual(10, len(raw_test_data))

        testData: list[OnlinePlayers] = []
        for i, e in enumerate(raw_test_data):  # Ensure unique ids
            as_dict = self._repo._adapt(e)
            as_dict["uuid"] = UUID(int=i).bytes
            testData.append(e.__class__(**as_dict))
        return testData
