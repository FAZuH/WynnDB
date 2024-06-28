from __future__ import annotations
from abc import ABC
from decimal import Decimal
from typing import Any, Iterable, TYPE_CHECKING

from sqlalchemy import Column, Tuple, delete, exists, select, text, tuple_
from sqlalchemy.schema import CreateTable

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..model import BaseModel
    from ... import BaseAsyncDatabase


class Repository[T: BaseModel, ID](ABC):

    def __init__(self, database: BaseAsyncDatabase[T], model_cls: type[T]) -> None:
        self._database = database
        self._model_cls = model_cls

    async def table_disk_usage(self, session: None | AsyncSession = None) -> Decimal:
        """
        Calculate the size of the table in bytes.

        Parameters
        ----------
        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.

        Returns
        -------
        Decimal
            Size of the table in bytes.
        """
        SQL = f"""
            SELECT
                ROUND(((data_length + index_length)), 2) AS "size_bytes"
            FROM
                information_schema.TABLES
            WHERE
                table_schema = :schema
                AND table_name = :table_name;
        """
        params = {
            "schema": self._database.database,
            "table_name": self.table_name
        }
        async with self._database.must_enter_session(session) as session:
            result = await session.execute(text(SQL), params)
            row = result.fetchone()
            ret = Decimal(row["size_bytes"]) if (row and row["size_bytes"] is not None) else Decimal(0)  # type: ignore
            return ret

    async def create_table(self, session: None | AsyncSession = None) -> None:
        """
        Create the table associated with the repository if it does not already exist.

        Parameters
        ----------
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        async with self.database.must_enter_session(session) as session:
            table = self.get_model_cls().get_table()
            stmt = CreateTable(table, if_not_exists=True)
            await session.execute(stmt)

    async def insert(self, entity: Iterable[T] | T, session: None | AsyncSession = None) -> None:
        """
        Insert one or more entities into the database.

        Parameters
        ----------
        entity : Iterable[T] | T
            An entity or an iterable of entities to be inserted into the database.
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        entities = self.__ensure_iterable(entity)
        async with self.database.must_enter_session(session) as session:
            session.add_all(entities)

    async def delete(self, id_: Iterable[ID] | ID, session: AsyncSession | None = None) -> None:
        """Deletes an entry from the repository based on `id_`

        Parameters
        ----------
        id_: Any
            Primary_key value of the entry to delete.

        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        model = self.get_model_cls()
        to_compare = self.__convert_comparable(id_)

        async with self.database.must_enter_session(session) as session:
            stmt = delete(model).where(self.__get_primary_key().in_(to_compare))
            await session.execute(stmt)

    async def is_exists(self, id_: ID, session: None | AsyncSession = None) -> bool:
        """
        Check if an entry with the given primary key exists in the database.

        Parameters
        ----------
        id_ : ID
            Primary key value of the entry to check.
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.

        Returns
        -------
        bool
            True if the entry exists, False otherwise.
        """
        async with self.database.must_enter_session(session) as session:
            stmt = select(exists().where(self.__get_primary_key() == (id_,)))
            result = await session.execute(stmt)
            is_exist = result.scalar()
            return is_exist or False

    def get_model_cls(self) -> type[T]:
        return self._model_cls

    @property
    def database(self) -> BaseAsyncDatabase[T]:
        return self._database

    @property
    def table_name(self) -> str:
        return self.get_model_cls().__tablename__

    def __get_primary_key(self) -> Tuple[Column[Any], ...]:
        model_cls = self.get_model_cls()
        primary_keys: tuple[Column[Any], ...] | Column[Any] = model_cls.__mapper__.primary_key
        if not isinstance(primary_keys, tuple):  # type: ignore
            tupl = tuple_(primary_keys)
        else:
            tupl = tuple_(*primary_keys)
        return tupl

    @staticmethod
    def __ensure_iterable[U](obj: Iterable[U] | U) -> Iterable[U]:
        if isinstance(obj, Iterable):
            return obj
        else:
            return [obj]

    def __convert_comparable(self, id_: Iterable[ID] | ID) -> list[tuple[ID, ...]]:
        ids = self.__ensure_iterable(id_)
        ret = [(id__,) for id__ in ids]
        return ret
