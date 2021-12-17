from typing import Type

from configcrunch import YamlConfigDocument, DocReference, variable_helper
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
                Optional('$name'): str,
                'template': str,
                Optional('pdf_template'): str,
                'system': str,
                'full_name': str,
                'short_description': str,
                'bg': str,
                Optional('stash'): dict,
                'spec': DocReference(Spec)
            }
        )

    @variable_helper
    def spec(self, name: str) -> Spec:
        if self.internal_get('spec').internal_contains(name):
            return self.internal_get('spec').internal_get(name)
        raise KeyError(f"Need spec {name}, but not defined for character.")

    def has_spec(self, name: str) -> bool:
        return name in self['spec']

    @classmethod
    def subdocuments(cls):
        return [
            ("spec", Spec)
        ]
