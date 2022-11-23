from configcrunch import DocReference
from schema import Schema, Optional

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs._ogl_aware import OglAware
from char_sheets.config.specs.ref_dnd5e.dnd_weapon import DndWeapon


SKILL_MAP = {
    "Acrobatics": "dex",
    "Animal Handling": "wis",
    "Arcana": "int",
    "Athletics": "str",
    "Deception": "cha",
    "History": "int",
    "Insight": "wis",
    "Intimidation": "cha",
    "Investigation": "int",
    "Medicine": "wis",
    "Nature": "int",
    "Perception": "wis",
    "Performance": "cha",
    "Persuasion": "cha",
    "Religion": "int",
    "Sleight of Hand": "dex",
    "Stealth": "dex",
    "Survival": "wis",
}


def build_dnd_skills():
    skls = {}
    for name in SKILL_MAP.keys():
        skls[name] = {
            'proficiency': bool,
            Optional('expertise'): bool,
            Optional('advantage'): bool,
            Optional('disadvantage'): bool,
            Optional('boon'): int
        }
    return skls


class Dnd5eSpec(AbstractSpec, OglAware):
    @classmethod
    def header(cls) -> str:
        return "dnd5e"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                'background': str,
                'inspiration': int,
                'proficiency': int,
                'boons': {
                    'saves': {
                        'str': int,
                        'dex': int,
                        'con': int,
                        'int': int,
                        'wis': int,
                        'cha': int
                    }
                },
                'death_saves': {
                    'successes': int,
                    'fails': int,
                },
                'proficiencies': {
                    'weapons': {
                        'simple': bool,
                        'martial': bool,
                        'unarmed': bool
                    },
                    'weapons_named': [str],
                    'tools': [str],
                    'armor': {
                        'light': bool,
                        'medium': bool,
                        'heavy': bool,
                        'shields': bool,
                    },
                    'saves': {
                        'str': bool,
                        'dex': bool,
                        'con': bool,
                        'int': bool,
                        'wis': bool,
                        'cha': bool
                    },
                },
                'weapons': [DocReference(DndWeapon)],
                'armor': {
                    'ac': int,
                    'name': str,
                    'stats': [str],
                },
                'skills': build_dnd_skills(),
                Optional('prepared_spells'): [str],
            }
        )

    @classmethod
    def subdocuments(cls):
        return [
            ("weapons[]", DndWeapon),
        ]

    def ac(self):
        return self["armor"]["ac"] + self.armor_bonus()

    def passive_insight(self):
        return 10 + self.skill_bonus("Insight") + (5 if "advantage" in self["skills"]["Insight"] and self["skills"]["Insight"]["advantage"] else 0) + (-5 if "disadvantage" in self["skills"]["Insight"] and self["skills"]["Insight"]["disadvantage"] else 0)

    def passive_investigation(self):
        return 10 + self.skill_bonus("Investigation") + (5 if "advantage" in self["skills"]["Investigation"] and self["skills"]["Investigation"]["advantage"] else 0) + (-5 if "disadvantage" in self["skills"]["Investigation"] and self["skills"]["Investigation"]["disadvantage"] else 0)

    def passive_perception(self):
        return 10 + self.skill_bonus("Perception") + (5 if "advantage" in self["skills"]["Perception"] and self["skills"]["Perception"]["advantage"] else 0) + (-5 if "disadvantage" in self["skills"]["Perception"] and self["skills"]["Perception"]["disadvantage"] else 0)

    def armor_bonus(self):
        ac = 0
        for stat in self["armor"]["stats"]:
            ac += getattr(self.parent().parent().spec('ogl'), stat + '_m')()
        return ac

    def save_bonus(self, save):
        return getattr(self.parent().parent().spec('ogl'), save + '_m')() + (self['proficiency'] if self['proficiencies']['saves'][save] else 0)

    def skill_attribute(self, skill):
        return SKILL_MAP[skill]

    def skill_attribute_bonus(self, skill):
        return getattr(self.parent().parent().spec('ogl'), self.skill_attribute(skill) + '_m')()

    def skill_bonus(self, skill_name):
        return self.skill_attribute_bonus(skill_name) + \
               (self['proficiency'] if self['skills'][skill_name]['proficiency'] else 0) + \
               (self['proficiency'] if 'expertise' in self['skills'][skill_name] and self['skills'][skill_name]['expertise'] else 0) + \
               (self['skills'][skill_name]['boon'] if 'boon' in self['skills'][skill_name] else 0)

    def spellcast_dc(self):
        return 10 + getattr(self.parent().parent().spec('ogl'), self.parent().parent().spec('ogl')['spellcasting_mod'] + '_m')() + self['proficiency']

    def weapon_proficiencies(self):
        ls = []
        if self['proficiencies']['weapons']['simple']:
            ls.append('Simple')
        if self['proficiencies']['weapons']['martial']:
            ls.append('Martial')
        if self['proficiencies']['weapons']['unarmed']:
            ls.append('Unarmed')
        ls.extend(self['proficiencies']['weapons_named'])
        return ', '.join(ls)

    def armor_proficiencies(self):
        ls = []
        if self['proficiencies']['armor']['light']:
            ls.append('Light')
        if self['proficiencies']['armor']['medium']:
            ls.append('Medium')
        if self['proficiencies']['armor']['heavy']:
            ls.append('Heavy')
        if self['proficiencies']['armor']['shields']:
            ls.append('Shields')
        return ', '.join(ls)

    def prepared_spells_count(self):
        # TODO: just wizard level!
        return getattr(self.parent().parent().spec('ogl'), self.parent().parent().spec('ogl')['spellcasting_mod'] + '_m')() + self.parent().parent().spec('ogl')['level']

    def prepared_spells_list(self):
        return ', '.join(self['prepared_spells'])

    def tool_proficiencies(self):
        return ', '.join(self['proficiencies']['tools'])
