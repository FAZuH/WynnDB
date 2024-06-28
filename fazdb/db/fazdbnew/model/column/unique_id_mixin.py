from abc import ABC
import hashlib
from typing import Any

from . import UuidColumn


class UniqueIdMixin(ABC):
        
    def __init__(self, unique_id: bytes | UuidColumn | None = None, *args: Any) -> None:
        encoded_variables = ''.join(list(map(str, args))).encode()
        hashed_variables = hashlib.sha256(encoded_variables).digest()
        self._unique_id = unique_id if isinstance(unique_id, UuidColumn) else UuidColumn(hashed_variables)

    @property
    def unique_id(self) -> UuidColumn:
        return self._unique_id

