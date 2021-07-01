from typing import Type

from configcrunch import YamlConfigDocument, DocReference, load_subdocument
from schema import Schema, Optional

from char_sheets.config.spec import Spec


class Character(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "character"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'template': str,
                'system': str,
                'full_name': str,
                'short_description': str,
                'bg': str,
                Optional('stash'): dict,
                'spec': DocReference(Spec)
            }
        )

    def spec(self, name: str) -> Spec:
        if name in self['spec']:
            return self['spec'][name]
        raise KeyError(f"Need spec {name}, but not defined for character.")

    def has_spec(self, name: str) -> bool:
        return name in self['spec']

    def _load_subdocuments(self, lookup_paths):
        if 'spec' in self:
            self['spec'] = load_subdocument(self['spec'], self, Spec, lookup_paths)
        return self
