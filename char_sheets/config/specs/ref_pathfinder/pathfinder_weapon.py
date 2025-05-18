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
                Optional('link'): str,
                Optional('hit_stat'): str,
            }
        )

    @classmethod
    def subdocuments(cls):
        return []

    def to_hit(self):
        if 'hit_stat' not in self or self['hit_stat'] == 'str':
            hit_bonus = self.parent().parent().parent().spec('ogl').str_m()
        elif self['hit_stat'] == 'dex':
            hit_bonus = self.parent().parent().parent().spec('ogl').dex_m()
        elif self['hit_stat'] == 'int':
            hit_bonus = self.parent().parent().parent().spec('ogl').int_m()
        elif self['hit_stat'] == 'wis':
            hit_bonus = self.parent().parent().parent().spec('ogl').wis_m()
        elif self['hit_stat'] == 'cha':
            hit_bonus = self.parent().parent().parent().spec('ogl').cha_m()

        return self.parent()['bab'] + hit_bonus + (self['fixed_plus_atk'] if 'fixed_plus_atk' in self else 0)

    def damage(self):
        return self['damage_dice'] + '+' + str(self.parent().parent().parent().spec('ogl').str_m() + (self['fixed_plus_dmg'] if 'fixed_plus_dmg' in self else 0))
