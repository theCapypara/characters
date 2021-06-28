from math import ceil, floor

from configcrunch import DocReference, REMOVE, load_subdocument
from schema import Schema, Optional, Or

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs.ref_dndpkmn.dndpkmn_ability import DndPkmnAbility
from char_sheets.config.specs.ref_dndpkmn.dndpkmn_attack import DndPkmnAttack


class ExtraCountersSpec(AbstractSpec):
    @classmethod
    def header(cls) -> str:
        return "extra_counters"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                'counters': [{
                    'name': str,
                    'available': Or(int, str),
                    Optional('max'): Or(int, str)
                }]
            }
        )
