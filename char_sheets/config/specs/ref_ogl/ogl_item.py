from configcrunch import YamlConfigDocument
from schema import Schema, Optional, Or


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
                Optional('weight'): Or(int, float),  # per piece
                Optional('notes'): str,
                Optional('link'): str,
            }
        )

    @classmethod
    def subdocuments(cls):
        return []
