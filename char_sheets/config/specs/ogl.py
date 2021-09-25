from math import floor

from configcrunch import DocReference, REMOVE, load_subdocument
from schema import Schema, Optional, Or

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs._has_ogl_like_inventory_trait import HasOglLikeInventoryTrait
from char_sheets.config.specs._ogl_aware import OglAware
from char_sheets.config.specs.ref_ogl.ogl_item import OglItem
from char_sheets.config.specs.ref_ogl.ogl_spell import OglSpell


class OglSpec(AbstractSpec, HasOglLikeInventoryTrait):
    @classmethod
    def header(cls) -> str:
        return "ogl"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                'class': str,
                'subclass': str,
                'level': int,
                'race': str,
                'alignment': str,
                'size_class': str,
                Optional('spellcasting_mod'): str,
                'stats': {
                    'str': int,
                    'dex': int,
                    'con': int,
                    'int': int,
                    'wis': int,
                    'cha': int
                },
                'movement': {
                    'land': int,
                    Optional('fly'): int,
                    Optional('swim'): int,
                    Optional('climb'): int
                },
                'vision': int,
                'current_hp': int,
                'max_hp': int,
                'hit_dice': int,
                'languages': [str],
                'race_abilities': [str],
                'class_abilities': [str],
                'extra_abilities': [str],
                'feats': [str],
                'inventory': {
                    'on_hand': [DocReference(OglItem)],
                    'stored': [DocReference(OglItem)],
                },
                'money': {
                    'gp': int,
                    'sp': int,
                    'cp': int,
                },
                'spell_slots': {
                    1: {'max': int, 'available': int},
                    2: {'max': int, 'available': int},
                    3: {'max': int, 'available': int},
                    4: {'max': int, 'available': int},
                    5: {'max': int, 'available': int},
                    6: {'max': int, 'available': int},
                    7: {'max': int, 'available': int},
                    8: {'max': int, 'available': int},
                    9: {'max': int, 'available': int},
                },
                Optional('known_spells'): int,
                'boons': {
                    'ac': int,
                    'ini': Or(int, str)
                },
                'spells': [DocReference(OglSpell)]
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
        if "spells" in self.doc and self["spells"] != REMOVE:
            lst = []
            for x in self["spells"]:
                lst.append(load_subdocument(x, self, OglSpell, lookup_paths))
            self["spells"] = lst
        return self

    def has_any_spells(self):
        for spell_slot in self['spell_slots'].values():
            if spell_slot['available'] > 0 or spell_slot['max'] > 0:
                return True
        return False

    def ac(self):
        matched_ac = None
        for spec in self.parent().doc.values():
            if isinstance(spec, OglAware):
                ac = spec.ac()
                if ac is not None:
                    if matched_ac:
                        raise ValueError("Multiple AC implementations for character found :(")
                    matched_ac = ac
        if matched_ac is None:
            return 10
        if self['boons']['ac']:
            matched_ac += self['boons']['ac']
        return matched_ac

    def ini(self):
        ini_boon = self['boons']['ini']
        if isinstance(ini_boon, str):
            ini_boon = self._mod(self['stats'][ini_boon])
        return self.dex_m() + ini_boon

    def str_m(self):
        return self._mod(self['stats']['str'])

    def dex_m(self):
        return self._mod(self['stats']['dex'])

    def con_m(self):
        return self._mod(self['stats']['con'])

    def int_m(self):
        return self._mod(self['stats']['int'])

    def wis_m(self):
        return self._mod(self['stats']['wis'])

    def cha_m(self):
        return self._mod(self['stats']['cha'])

    def _mod(self, x):
        return floor((x - 10) / 2)

    def has_complex_movement(self):
        return 'swim' in self['movement'] or 'fly' in self['movement'] or 'climb' in self['movement']
