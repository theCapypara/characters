from configcrunch import YamlConfigDocument
from schema import Schema, Optional, Or

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
                Optional('link'): str,
                Optional('special'): str,
                'level': int,
                Optional('components'): str,
                'casting_time': str,
                'range': Or(int, str),
                'duration': str,
                Optional('save'): str,
                Optional('resistance'): str,
                'description': str,
            }
        )

    @classmethod
    def subdocuments(cls):
        return []

    def range_text(self):
        if isinstance(self['range'], str):
            return self['range']
        if self['range'] == 0:
            return 'Touch'
        if self['range'] == -1:
            return 'Self'
        return size(None, self['range'])
