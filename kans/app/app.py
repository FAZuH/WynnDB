from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from kans import Api, Database, Config, Heartbeat, Logger


class App(Protocol):
    """<<interface>>"""
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def api(self) -> Api: ...
    @property
    def config(self) -> Config: ...
    @property
    def db(self) -> Database: ...
    @property
    def heartbeat(self) -> Heartbeat: ...
    @property
    def logger(self) -> Logger: ...
