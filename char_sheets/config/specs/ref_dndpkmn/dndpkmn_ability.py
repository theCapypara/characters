from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class DndPkmnAbility(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "dndpkmn_ability"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'description': str
            }
        )

    @classmethod
    def subdocuments(cls):
        return []
