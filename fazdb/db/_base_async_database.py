from __future__ import annotations
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator, TYPE_CHECKING

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession
    from sqlalchemy.orm import DeclarativeBase


class BaseAsyncDatabase[T: DeclarativeBase](ABC):

    def __init__(
            self,
            driver: str,
            user: str,
            password: str,
            host: str,
            port: int,
            database: str,
        ) -> None:
        self._driver = driver
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database

        url = URL.create(
            driver,
            user,
            password,
            host,
            port,
            database
        )
        self._engine = create_async_engine(url)

    @asynccontextmanager
    async def enter_connection(self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.engine.connect() as conn:
            yield conn

    @asynccontextmanager
    async def enter_session(self) -> AsyncGenerator[AsyncSession, None]:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session.begin() as session:
            yield session

    @asynccontextmanager
    async def must_enter_connection(self, connection: AsyncConnection | None = None) -> AsyncGenerator[AsyncConnection, None]:
        if connection:
            yield connection
        else:
            async with self.enter_connection() as connection:
                yield connection

    @asynccontextmanager
    async def must_enter_session(self, session: AsyncSession | None = None) -> AsyncGenerator[AsyncSession, None]:
        if session:
            yield session
        else:
            async with self.enter_session() as session:
                yield session

    async def create_all(self) -> None:
        async with self.enter_connection() as connection:
            await connection.run_sync(self.base_model.metadata.create_all)

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def driver(self) -> str:
        return self._driver

    @property
    def user(self) -> str:
        return self._user

    @property
    def password(self) -> str:
        return self._password

    @property
    def host(self) -> str:
        return self._host

    @property
    def database(self) -> str:
        return self._database

    @property
    @abstractmethod
    def base_model(self) -> T: ...

