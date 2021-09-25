from configcrunch import YamlConfigDocument
from schema import Schema, Optional, Or

SkillRequiredSpec = {
    'skill': str, 'damage_type': str, 'skill_amount': int, Optional('misc_requirement'): str
}
RangedSkillRequiredSpec = {
    'skill': str, 'range': int, 'skill_amount': int, Optional('misc_requirement'): str
}


class AnimaliaWeapon(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "weapon"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'two_handed': bool,
                'dice': str,
                'actions': {
                    Optional('thrust'): SkillRequiredSpec,
                    Optional('slash'): SkillRequiredSpec,
                    Optional('stab'): SkillRequiredSpec,

                    Optional('punch'): SkillRequiredSpec,
                    Optional('kick'): SkillRequiredSpec,
                    Optional('whip'): SkillRequiredSpec,
                    Optional('claw'): SkillRequiredSpec,
                    Optional('headbutt'): SkillRequiredSpec,

                    Optional('pierce'): SkillRequiredSpec,
                    Optional('throw'): RangedSkillRequiredSpec,

                    Optional('parry'): {
                        'skill': str, 'skill_amount': int
                    },

                    Optional('advanced'): {
                        str: str
                    }
                }
            }
        )
