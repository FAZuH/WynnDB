from typing import Any
from . import CharacterInfoId
from .. import UuidColumn


class CharacterInfo(CharacterInfoId):
    """implements ``CharacterInfoId``

    id: `character_uuid`"""

    def __init__(self, character_uuid: bytes | UuidColumn, uuid: bytes | UuidColumn, type: str) -> None:
        super().__init__(character_uuid)
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._type = type

    def to_dict(self) -> dict[str, Any]:
        """Converts the instance to a tuple.
        The order of the elements is the same as the order of the class constructor."""
        return {
                "character_uuid": self.character_uuid.uuid,
                "uuid": self.uuid.uuid,
                "type": self.type
        }

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def type(self) -> str:
        return self._type
