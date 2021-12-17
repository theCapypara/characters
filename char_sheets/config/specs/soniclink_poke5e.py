from configcrunch import DocReference, REMOVE
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

    @classmethod
    def subdocuments(cls):
        return [
            ("attacks[]", SoniclinkPoke5eAttack),
        ]
