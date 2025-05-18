from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class PathfinderArmor(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "pathfinder_armor"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'bonus': int,
                'minus': int,
                'max_dex': int,
                'arcane_fail_chance': int,
                Optional('weight'): int,
                'type': str,
                Optional('link'): str,
                Optional('notes'): str,
            }
        )

    @classmethod
    def subdocuments(cls):
        return []
