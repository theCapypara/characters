from typing import List

from configcrunch import DocReference
from schema import Schema, Optional

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs._has_ogl_like_inventory_trait import HasOglLikeInventoryTrait
from char_sheets.config.specs.ref_animalia.armor import AnimaliaArmor
from char_sheets.config.specs.ref_animalia.talent import AnimaliaTalent
from char_sheets.config.specs.ref_animalia.weapon import AnimaliaWeapon
from char_sheets.config.specs.ref_ogl.ogl_item import OglItem


class AnimaliaSpec(AbstractSpec, HasOglLikeInventoryTrait):

    @classmethod
    def header(cls) -> str:
        return "animalia"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                'race': str,
                'species': str,
                'subspecies': str,
                'current_hp': int,
                'max_hp': int,
                'stats': {
                    'arm': int,
                    'leg': int,
                    'head': int,
                    'soul': int
                },
                'house': str,
                'languages': [str],
                'talents': {
                    'arm': [DocReference(AnimaliaTalent)],
                    'leg': [DocReference(AnimaliaTalent)],
                    'head': [DocReference(AnimaliaTalent)],
                    'soul': [DocReference(AnimaliaTalent)],
                    'species': [DocReference(AnimaliaTalent)],
                    'subspecies': [DocReference(AnimaliaTalent)],
                },
                'weapons': [DocReference(AnimaliaWeapon)],
                'armor': [DocReference(AnimaliaArmor)],
                'inventory': {
                    'on_hand': [DocReference(OglItem)],
                    'stored': [DocReference(OglItem)],
                },
                'money': {
                    'gp': int,
                    'sp': int,
                    'cp': int,
                },
                'boons': {
                    'ac': int
                }
            }
        )

    @classmethod
    def subdocuments(cls):
        return [
            ("inventory/on_hand[]", OglItem),
            ("inventory/stored[]", OglItem),
            ("weapons[]", AnimaliaWeapon),
            ("armor[]", AnimaliaArmor),
            ("talents/arm[]", AnimaliaTalent),
            ("talents/leg[]", AnimaliaTalent),
            ("talents/head[]", AnimaliaTalent),
            ("talents/soul[]", AnimaliaTalent),
            ("talents/species[]", AnimaliaTalent),
            ("talents/subspecies[]", AnimaliaTalent),
        ]

    def ac(self):
        base = self["boons"]["ac"]
        for armor in self["armor"]:
            base += armor["armor"]
        return base
