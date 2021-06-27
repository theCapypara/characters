from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class SoniclinkPoke5eAttack(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "soniclink_poke5e_attack"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'pp': {
                    'max': int,
                    'available': int
                },
                'target': str,
                'range': int,
                'description': str,
            }
        )
