from math import ceil, floor

from configcrunch import DocReference
from schema import Schema, Optional

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs.ref_dndpkmn.dndpkmn_ability import DndPkmnAbility
from char_sheets.config.specs.ref_dndpkmn.dndpkmn_attack import DndPkmnAttack


NATURE_MAP = {
    "lonely": ("str", "con"),
    "adamant": ("str", "dex"),
    "brave": ("str", "int"),
    "naughty": ("str", "wis"),
    "bashful": ("str", "cha"),
    "timid": ("dex", "str"),
    "hasty": ("dex", "con"),
    "jolly": ("dex", "int"),
    "naive": ("dex", "wis"),
    "focused": ("dex", "cha"),
    "bold": ("con", "str"),
    "relaxed": ("con", "dex"),
    "impish": ("con", "int"),
    "lax": ("con", "wis"),
    "callous": ("con", "cha"),
    "modest": ("int", "str"),
    "mild": ("int", "con"),
    "quiet": ("int", "dex"),
    "rash": ("int", "wis"),
    "serious": ("int", "cha"),
    "calm": ("wis", "str"),
    "gentle": ("wis", "con"),
    "sassy": ("wis", "dex"),
    "careful": ("wis", "int"),
    "docile": ("wis", "cha"),
    "smooth": ("cha", "str"),
    "quirky": ("cha", "int"),
    "hardy": ("cha", "wis"),
    "cocky": ("cha", "dex"),
    "fragile": ("cha", "con"),
}


class DndPkmn(AbstractSpec):
    @classmethod
    def header(cls) -> str:
        return "dndpkmn"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('evolution_level'): int,
                'types': [str],
                'current_pp': int,
                'boons': {
                    'pp': int,
                },
                'nature': str,
                'ability': DocReference(DndPkmnAbility),
                'attacks': [DocReference(DndPkmnAttack)]
            }
        )

    @classmethod
    def subdocuments(cls):
        return [
            ("ability", DndPkmnAbility),
            ("attacks[]", DndPkmnAttack)
        ]

    def nature_plus(self):
        return NATURE_MAP[self['nature']][0]

    def nature_minus(self):
        return NATURE_MAP[self['nature']][1]

    def max_pp(self):
        return floor(self.parent().parent().spec('ogl')['level'] / 2) + (2 * self.parent().parent().spec('dnd5e')['proficiency']) + self['boons']['pp']
