from typing import List

from configcrunch import DocReference, REMOVE, load_subdocument
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

    def _load_subdocuments(self, lookup_paths):
        if "inventory" in self.doc and self["inventory"] != REMOVE:
            if "on_hand" in self.doc["inventory"] and self["inventory"]["on_hand"] != REMOVE:
                lst = []
                for x in self["inventory"]["on_hand"]:
                    lst.append(load_subdocument(x, self, OglItem, lookup_paths))
                self["inventory"]["on_hand"] = lst
            if "stored" in self.doc["inventory"] and self["inventory"]["stored"] != REMOVE:
                lst = []
                for x in self["inventory"]["stored"]:
                    lst.append(load_subdocument(x, self, OglItem, lookup_paths))
                self["inventory"]["stored"] = lst
        if "weapons" in self.doc and self["weapons"] != REMOVE:
            lst = []
            for x in self["weapons"]:
                lst.append(load_subdocument(x, self, AnimaliaWeapon, lookup_paths))
            self["weapons"] = lst
        if "armor" in self.doc and self["armor"] != REMOVE:
            lst = []
            for x in self["armor"]:
                lst.append(load_subdocument(x, self, AnimaliaArmor, lookup_paths))
            self["armor"] = lst
        if "talents" in self.doc and self["talents"] != REMOVE:
            if "arm" in self.doc["talents"] and self["talents"]["arm"] != REMOVE:
                lst = []
                for x in self["talents"]["arm"]:
                    lst.append(load_subdocument(x, self, AnimaliaTalent, lookup_paths))
                self["talents"]["arm"] = lst
            if "leg" in self.doc["talents"] and self["talents"]["leg"] != REMOVE:
                lst = []
                for x in self["talents"]["leg"]:
                    lst.append(load_subdocument(x, self, AnimaliaTalent, lookup_paths))
                self["talents"]["leg"] = lst
            if "head" in self.doc["talents"] and self["talents"]["head"] != REMOVE:
                lst = []
                for x in self["talents"]["head"]:
                    lst.append(load_subdocument(x, self, AnimaliaTalent, lookup_paths))
                self["talents"]["head"] = lst
            if "soul" in self.doc["talents"] and self["talents"]["soul"] != REMOVE:
                lst = []
                for x in self["talents"]["soul"]:
                    lst.append(load_subdocument(x, self, AnimaliaTalent, lookup_paths))
                self["talents"]["soul"] = lst
            if "species" in self.doc["talents"] and self["talents"]["species"] != REMOVE:
                lst = []
                for x in self["talents"]["species"]:
                    lst.append(load_subdocument(x, self, AnimaliaTalent, lookup_paths))
                self["talents"]["species"] = lst
            if "subspecies" in self.doc["talents"] and self["talents"]["subspecies"] != REMOVE:
                lst = []
                for x in self["talents"]["subspecies"]:
                    lst.append(load_subdocument(x, self, AnimaliaTalent, lookup_paths))
                self["talents"]["subspecies"] = lst
        return self

    def ac(self):
        base = self["boons"]["ac"]
        for armor in self["armor"]:
            base += armor["armor"]
        return base
