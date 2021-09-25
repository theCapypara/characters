from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class AnimaliaTalent(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "talent"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'description': str,
                'type': str,
                'level': int,
            }
        )
