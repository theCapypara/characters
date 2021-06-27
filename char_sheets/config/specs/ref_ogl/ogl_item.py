from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class OglItem(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "ogl_item"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                Optional('count'): int,
                Optional('weight'): int,  # per piece
                Optional('notes'): str,
            }
        )
