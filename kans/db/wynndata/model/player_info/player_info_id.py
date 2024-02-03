from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from kans import UuidColumn


class PlayerInfoId(Protocol):
    @property
    def uuid(self) -> UuidColumn: ...
