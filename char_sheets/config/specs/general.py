from configcrunch import DocReference
from schema import Schema, Optional, Or

from char_sheets.config.specs import AbstractSpec
from char_sheets.config.specs.ref_general.story_log import StoryLog


class GeneralSpec(AbstractSpec):
    @classmethod
    def header(cls) -> str:
        return "general"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'gender': str,
                'images': [str],
                Optional('image_credits'): str,
                Optional('home'): str,
                Optional('size'): Or(int, float),
                Optional('weight'): Or(int, float),
                Optional('eye_color'): str,
                Optional('hair_color'): str,
                Optional('age'): int,
                Optional('lore'): {
                    Optional('personality'): str,
                    Optional('backstory'): str,
                    Optional('bonds'): str,
                    Optional('strengths'): str,
                    Optional('flaws'): str,
                    Optional('ideals'): str,
                    Optional('extra'): str,
                    #Optional('story_log'): [DocReference(StoryLog)],
                }
            }
        )

    @classmethod
    def subdocuments(cls):
        return [
            #("lore/story_log", StoryLog)
        ]

    def count_optional(self):
        count = 0
        if 'home' in self:
            count += 1
        if 'size' in self:
            count += 1
        if 'weight' in self:
            count += 1
        if 'eye_color' in self:
            count += 1
        if 'hair_color' in self:
            count += 1
        if 'age' in self:
            count += 1
        return count
