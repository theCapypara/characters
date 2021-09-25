from configcrunch import YamlConfigDocument
from schema import Schema, Optional

from char_sheets.ui_methods import p


class DndWeapon(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "dnd_weapon"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'finese': bool,
                Optional('use_int'): bool,
                'ranged': bool,
                'wpn_type': str,
                'dmg_type': str,
                'damage_dice': str,
                Optional('fixed_plus_dmg'): int,
                Optional('fixed_plus_atk'): int,
                Optional('ammo'): int,
                Optional('notes'): str,
                Optional('range'): {
                    'normal': int,
                    'better': int
                },
            }
        )

    def to_hit(self):
        prof = self.parent()['proficiency'] if self.parent()['proficiencies']['weapons'][self['wpn_type']] else 0
        if 'use_int' in self and self['use_int']:
            m = self.parent().parent().parent().spec('ogl').int_m()
        else:
            mstr = self.parent().parent().parent().spec('ogl').str_m() if not self['ranged'] else 0
            mdex = self.parent().parent().parent().spec('ogl').dex_m() if self['ranged'] or self['finese'] else 0
            m = max(mstr, mdex)
        return prof + m + (self['fixed_plus_atk'] if 'fixed_plus_atk' in self else 0)

    def damage(self):
        if 'use_int' in self and self['use_int']:
            m = self.parent().parent().parent().spec('ogl').int_m()
        else:
            mstr = self.parent().parent().parent().spec('ogl').str_m() if not self['ranged'] else 0
            mdex = self.parent().parent().parent().spec('ogl').dex_m() if self['ranged'] or self['finese'] else 0
            m = max(mstr, mdex)
        return self['damage_dice'] + '+' + str(m + (self['fixed_plus_dmg'] if 'fixed_plus_dmg' in self else 0))

    def attributes(self):
        attrs = [p(None, self['wpn_type'])]
        if self['finese']:
            attrs += ['F']
        if self['ranged']:
            attrs += ['R']
        return ', '.join(attrs)

    def range(self):
        if 'range' not in self:
            return ''
        return str(self['range']['normal']) + ' / ' + str(self['range']['better'])
