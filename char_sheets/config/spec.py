from abc import ABC
from typing import Type

from configcrunch import YamlConfigDocument, load_subdocument, REMOVE, DocReference
from schema import Schema, Optional

from char_sheets.config.specs import AbstractSpec


def get_spec_reference_type(name: str) -> Type[AbstractSpec]:
    try:
        name = f"char_sheets.config.specs.{name}"
        mod = __import__(name, fromlist=[''])
        for obj in mod.__dict__.values():
            if isinstance(obj, type) and issubclass(obj, AbstractSpec) and obj != AbstractSpec:
                return obj
    except:
        pass
    raise ValueError(f"Spec for char_sheets.config.spec.{name} not found.")


class Spec(YamlConfigDocument, ABC):
    @classmethod
    def header(cls) -> str:
        return "spec"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                str: DocReference(AbstractSpec)
            }
        )

    def _load_subdocuments(self, lookup_paths):
        for key, doc in self.items():
            if doc != REMOVE:
                self[key] = load_subdocument(doc, self, get_spec_reference_type(key), lookup_paths)
        return self
