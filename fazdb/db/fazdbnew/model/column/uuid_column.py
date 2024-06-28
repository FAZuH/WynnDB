from __future__ import annotations
from uuid import UUID


class UuidColumn:

    def __init__(self, uuid_: bytes) -> None:
        self._uuid: bytes = uuid_

    @classmethod
    def from_str(cls, uuid: str) -> UuidColumn:
        return cls(UUID(uuid).bytes)

    def to_str(self, hypen: bool = True) -> str:
        return str(UUID(bytes=self._uuid)) if hypen else UUID(bytes=self._uuid).hex

    @property
    def uuid(self) -> bytes:
        return self._uuid
