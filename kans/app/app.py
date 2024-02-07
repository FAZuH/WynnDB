from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from loguru import Logger
    from kans import Database, Api


class App(Protocol):
    @property
    def config(self) -> dict[str, str]: ...
    @property
    def logger(self) -> Logger: ...
    @property
    def wynnapi(self) -> Api: ...
    @property
    def wynnrepo(self) -> Database: ...
