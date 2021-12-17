from configcrunch import YamlConfigDocument
from schema import Schema, Optional


class DndPkmnAttack(YamlConfigDocument):
    @classmethod
    def header(cls) -> str:
        return "dndpkmn_attack"

    @classmethod
    def schema(cls) -> Schema:
        return Schema(
            {
                Optional('$ref'): str,
                'name': str,
                'description': str,
                'type': str,
                'atk_bonus_or_save': {
                    Optional('dice'): str,
                    Optional('fixed'): int,
                    Optional('stats'): [str]
                },
                Optional('save'): str,
                'pp': int,
                'target': str,
                'range': int
            }
        )

    @classmethod
    def subdocuments(cls):
        return []

    def atk_bonus_or_save(self):
        dice = self['atk_bonus_or_save']['dice'] + '+' if 'dice' in self['atk_bonus_or_save'] else ''
        fixed = self['atk_bonus_or_save']['fixed'] if 'dice' in self['atk_bonus_or_save'] else 0
        stats = 0
        stab = 2 if self['type'] in self.parent()['types'] else 0
        for stat in self['atk_bonus_or_save']['stats']:
            stats += getattr(self.parent().parent().parent().spec('ogl'), stat + '_m')()
        return dice + str(stab + fixed + stats + self.parent().parent().parent().spec('dnd5e')['proficiency'])
