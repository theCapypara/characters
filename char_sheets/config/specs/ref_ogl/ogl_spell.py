from configcrunch import YamlConfigDocument
from schema import Schema, Optional

from char_sheets.ui_methods import size


class OglSpell(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "ogl_spell"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                Optional('special'): str,
                'level': int,
                Optional('components'): str,
                'casting_time': str,
                'range': int,
                'duration': str,
                Optional('save'): str,
                'description': str,
            }
        )

    @classmethod
    def subdocuments(cls):
        return []

    def range_text(self):
        if self['range'] == 0:
            return 'Touch'
        if self['range'] == -1:
            return 'Self'
        return size(None, self['range'])
