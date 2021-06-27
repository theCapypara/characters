from configcrunch import DocReference, REMOVE, load_subdocument
from schema import Schema, Optional

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs.ref_soniclink_poke5e.soniclink_poke5e_attack import SoniclinkPoke5eAttack


class Poke5e(AbstractSpec):
    @classmethod
    def header(cls) -> str:
        return "soniclink_poke5e"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                'types': [str],
                'attacks': [DocReference(SoniclinkPoke5eAttack)]
            }
        )

    def _load_subdocuments(self, lookup_paths):
        if "attacks" in self.doc and self["attacks"] != REMOVE:
            lst = []
            for x in self["attacks"]:
                lst.append(load_subdocument(x, self, SoniclinkPoke5eAttack, lookup_paths))
            self["attacks"] = lst
        return self
