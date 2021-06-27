from typing import Optional

from configcrunch import YamlConfigDocument, DocReference, REMOVE, load_subdocument
from schema import Schema

from char_sheets.config.character import Character


class Characters(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "characters"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                str: DocReference(Character)
            }
        )

    def get(self, name) -> Optional[Character]:
        if name in self.doc:
            return self.doc[name]
        return None

    def _load_subdocuments(self, lookup_paths):
        for key, doc in self.items():
            if doc != REMOVE:
                self[key] = load_subdocument(doc, self, Character, lookup_paths)
        return self
