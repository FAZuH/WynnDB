from .column import UuidColumn


class CharacterInfo:

    def __init__(self, character_uuid: bytes | UuidColumn, uuid: bytes | UuidColumn, type: str) -> None:
        self._character_uuid = character_uuid if isinstance(character_uuid, UuidColumn) else UuidColumn(character_uuid)
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._type = type

    @property
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def type(self) -> str:
        return self._type
