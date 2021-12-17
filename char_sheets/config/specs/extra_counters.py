from schema import Schema, Optional, Or

from char_sheets.config.specs import AbstractSpec


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

    @classmethod
    def subdocuments(cls):
        return []
