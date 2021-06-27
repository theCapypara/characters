from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class StoryLog(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "story_log"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                Optional(str): str,
                'text': str,
            }
        )
