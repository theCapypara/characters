from configcrunch import YamlConfigDocument
from schema import Schema, Optional, Or


class AnimaliaArmor(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "armor"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'armor': int,
                'hands': int,
                'skill_required': Or(True, {
                    'skill': str, 'skill_amount': int
                }),
                'combination_possible': bool,
                'weakness': [str],
                'resistance': [str],
            }
        )
