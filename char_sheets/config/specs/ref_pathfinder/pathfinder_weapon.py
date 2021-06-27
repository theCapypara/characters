from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class PathfinderWeapon(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "pathfinder_weapon"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'crit_mod': int,
                'crit_min': int,
                'damage_dice': str,
                Optional('fixed_plus_dmg'): int,
                Optional('fixed_plus_atk'): int,
                Optional('notes'): str,
                Optional('range'): int,
                Optional('weight'): int,
            }
        )

    def to_hit(self):
        return self.parent()['bab'] + self.parent().parent().parent().spec('ogl').str_m() + (self['fixed_plus_atk'] if 'fixed_plus_atk' in self else 0)

    def damage(self):
        return self['damage_dice'] + '+' + str(self.parent().parent().parent().spec('ogl').str_m() + (self['fixed_plus_dmg'] if 'fixed_plus_dmg' in self else 0))
