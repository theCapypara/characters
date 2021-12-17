from typing import Optional

from configcrunch import YamlConfigDocument, DocReference
from schema import Schema

from char_sheets.config.character import Character


class Characters(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "characters"

    @classmethod
    def schema(cls) -> Schema:
        return Schema({"characters": {
            str: DocReference(Character)
        }})

    def get(self, name) -> Optional[Character]:
        if name in self.doc:
            return self.doc[name]
        return None

    @classmethod
    def subdocuments(cls):
        return [
            ("characters[]", Character)
        ]
