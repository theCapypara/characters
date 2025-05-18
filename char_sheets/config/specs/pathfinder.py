from configcrunch import DocReference, REMOVE
from schema import Schema, Optional

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs._ogl_aware import OglAware
from char_sheets.config.specs.ref_pathfinder.pathfinder_armor import PathfinderArmor
from char_sheets.config.specs.ref_pathfinder.pathfinder_weapon import PathfinderWeapon

SKILL_MAP = {
    "Acrobatics":                   ("dex", False, "Akrobatik"),
    "Appraise":                     ("int", False, "Schätzen"),
    "Bluff":                        ("cha", False, "Bluffen"),
    "Climb":                        ("str", False, "Klettern"),
    "Craft":                        ("int", False, "Handwerk"),
    "Diplomacy":                    ("cha", False, "Diplomatie"),
    "Disable Device":               ("dex", True,  "Mechanismus ausschalten"),
    "Disguise":                     ("cha", False, "Verkleiden"),
    "Escape Artist":                ("dex", False, "Entfesselungskunst"),
    "Fly":                          ("dex", False, "Fliegen"),
    "Handle Animal":                ("cha", True,  "Mit Tieren umgehen"),
    "Heal":                         ("wis", False, "Heilkunde"),
    "Intimidate":                   ("cha", False, "Einschüchtern"),
    "Knowledge (arcana)":           ("int", True,  "Wissen (Arkanes)"),
    "Knowledge (dungeoneering)":    ("int", True,  "Wissen (Gewölbekunde)"),
    "Knowledge (engineering)":      ("int", True,  "Wissen (Baukunst)"),
    "Knowledge (geography)":        ("int", True,  "Wissen (Geographie)"),
    "Knowledge (history)":          ("int", True,  "Wissen (Geschichte)"),
    "Knowledge (local)":            ("int", True,  "Wissen (Lokales)"),
    "Knowledge (nature)":           ("int", True,  "Wissen (Natur)"),
    "Knowledge (nobility)":         ("int", True,  "Wissen (Adel und Königshäuser)"),
    "Knowledge (planes)":           ("int", True,  "Wissen (Die Ebenen)"),
    "Knowledge (religion)":         ("int", True,  "Wissen (Religion)"),
    "Linguistics":                  ("int", False, "Sprachenkunde"),
    "Perception":                   ("wis", False, "Wahrnehmung"),
    "Perform":                      ("cha", False, "Auftreten"),
    "Profession":                   ("wis", True,  "Beruf"),
    "Ride":                         ("dex", False, "Reiten"),
    "Sense Motive":                 ("wis", False, "Motiv erkennen"),
    "Sleight of Hand":              ("dex", True,  "Fingerfertigkeit"),
    "Spellcraft":                   ("int", True,  "Zauberkunde"),
    "Stealth":                      ("dex", False, "Heimlichkeit"),
    "Survival":                     ("wis", False, "Überlebenskunst"),
    "Swim":                         ("str", False, "Schwimmen"),
    "Use Magic Device":             ("cha", True,  "Magischen Gegenstand benutzen"),
}


def build_pathfinder_skills():
    skls = {}
    for name in SKILL_MAP.keys():
        skls[name] = {
            'class_skill': bool,
            'ranks': int,
            Optional('boon'): int,
            Optional('type'): str,
            Optional('usable_untrained'): bool
        }
    return skls


class PathfinderSpec(AbstractSpec, OglAware):
    @classmethod
    def header(cls) -> str:
        return "pathfinder"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                'bab': int,
                'natural_ac': int,
                'save_base': {
                    'reflex': int,
                    'will': int,
                    'fortitude': int
                },
                'boons': {
                    'cmb': int,
                    'cmd': int,
                    'saves': {
                        'reflex': int,
                        'will': int,
                        'fortitude': int
                    }
                },
                Optional('known_spells'): {
                    Optional('0'): int,
                    Optional('1'): int,
                    Optional('2'): int,
                    Optional('3'): int,
                    Optional('4'): int,
                    Optional('5'): int,
                    Optional('6'): int,
                    Optional('7'): int,
                    Optional('8'): int,
                    Optional('9'): int,
                },
                'weapons': [DocReference(PathfinderWeapon)],
                'armor': [DocReference(PathfinderArmor)],
                'skills': build_pathfinder_skills(),
            }
        )

    @classmethod
    def subdocuments(cls):
        return [
            ("weapons[]", PathfinderWeapon),
            ("armor[]", PathfinderArmor),
        ]

    def ac(self):
        # TODO Size mod
        return 10 + \
               sum(x["bonus"] for x in self["armor"]) + \
               self.parent().parent().spec('ogl').dex_m() + \
               self["natural_ac"] + \
               self.parent().parent().spec('ogl')["boons"]["ac"]

    def cmb(self):
        # TODO Size mod
        return self["bab"] + self.parent().parent().spec('ogl').str_m()

    def cmd(self):
        return 10 + \
               self["bab"] + self.parent().parent().spec('ogl').str_m() + \
               self.parent().parent().spec('ogl').dex_m()

    def save_attribute(self, save):
        if save == 'reflex':
            return 'dex'
        if save == 'will':
            return 'wis'
        if save == 'fortitude':
            return 'con'

    def save_attribute_bonus(self, save):
        return getattr(self.parent().parent().spec('ogl'), self.save_attribute(save) + '_m')()

    def save_boon(self, save, print=True):
        v = self['boons']['saves'][save]
        if not print:
            return v
        return v if v > 0 else ''

    def save_bonus(self, save):
        return self['save_base'][save] + self.save_attribute_bonus(save) + self.save_boon(save, False)

    def skill_attribute(self, skill):
        return SKILL_MAP[skill][0]

    def skill_attribute_bonus(self, skill):
        return getattr(self.parent().parent().spec('ogl'), self.skill_attribute(skill) + '_m')()

    def skill_bonus(self, skill_name):
        skill = self["skills"][skill_name]
        class_bonus = 3 if skill['ranks'] > 0 and skill['class_skill'] else 0
        if not ("usable_untrained" in skill and skill["usable_untrained"]) and SKILL_MAP[skill_name][1] and skill['ranks'] < 1:  # Needs training
            return -99
        return self.skill_attribute_bonus(skill_name) + skill['ranks'] + (skill['boon'] if 'boon' in skill else 0) + class_bonus

    def spellcast_dc(self, level: int):
        return 10 + getattr(self.parent().parent().spec('ogl'), self.parent().parent().spec('ogl')['spellcasting_mod'] + '_m')() + level
