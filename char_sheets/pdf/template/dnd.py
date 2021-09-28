import os
from typing import Union

from char_sheets.config.character import Character
from char_sheets.pdf.template.abstract import AbstractPdfTemplate, process_pdf_form_fields, pdf_get


class DndPdfTemplate(AbstractPdfTemplate):
    def __init__(self, character: Character):
        super().__init__(character)
        weapon_data = self._weapons()
        class_level = pdf_get(self.character.spec('ogl'), 'class') + ' ' + str(pdf_get(self.character.spec('ogl'), 'level'))
        self.mapping = {
            'CharacterName': self.character['full_name'],
            'CharacterName 2': self.character['full_name'],
            'Age': pdf_get(self.character.spec('general'), 'age'),
            'Height': pdf_get(self.character.spec('general'), 'size'),
            'Weight': pdf_get(self.character.spec('general'), 'weight'),
            'Eyes': pdf_get(self.character.spec('general'), 'eye_color'),
            'Hair': pdf_get(self.character.spec('general'), 'hair_color'),
            'Spellcasting Class 2': class_level,
            'ClassLevel': class_level,
            'SpellcastingAbility 2': pdf_get(self.character.spec('general'), 'spellcasting_mod'),
            'SpellSaveDC  2': character.spec('dnd5e').spellcast_dc(),
            'Background': pdf_get(self.character.spec('dnd5e'), 'background'),
            'PlayerName': 'Capypara',
            'Race': pdf_get(self.character.spec('ogl'), 'race'),
            'Alignment': pdf_get(self.character.spec('ogl'), 'alignment'),
            'Inspiration': pdf_get(self.character.spec('dnd5e'), 'inspiration'),
            'ProfBonus': pdf_get(self.character.spec('dnd5e'), 'proficiency'),
            'AC': self.character.spec('ogl').ac(),
            'Initiative': self.character.spec('ogl').ini(),
            'Speed': pdf_get(self.character.spec('ogl'), 'movement', 'land'),
            'PersonalityTraits': pdf_get(self.character.spec('general'), 'lore', 'personality'),
            'Ideals': pdf_get(self.character.spec('general'), 'lore', 'ideals'),
            'Bonds': pdf_get(self.character.spec('general'), 'lore', 'bonds'),
            'Flaws': pdf_get(self.character.spec('general'), 'lore', 'flaws'),
            'HPMax': pdf_get(self.character.spec('ogl'), 'hp_max'),
            'HPCurrent': pdf_get(self.character.spec('ogl'), 'hp_current'),
            'HD': pdf_get(self.character.spec('ogl'), 'hit_dice'),  # hit dice
            'Check Box 12': self.character.spec('dnd5e')['death_saves']['successes'] > 0,  # Death Save Success 1
            'Check Box 13': self.character.spec('dnd5e')['death_saves']['successes'] > 1,  # Death Save Success 2
            'Check Box 14': self.character.spec('dnd5e')['death_saves']['successes'] > 2,  # Death Save Success 3
            'Check Box 15': self.character.spec('dnd5e')['death_saves']['fails'] > 0,  # Death Fail Success 1
            'Check Box 16': self.character.spec('dnd5e')['death_saves']['fails'] > 1,  # Death Fail Success 2
            'Check Box 17': self.character.spec('dnd5e')['death_saves']['fails'] > 2,  # Death Fail Success 3
            'STR': pdf_get(self.character.spec('ogl'), 'stats', 'str'),
            'DEX': pdf_get(self.character.spec('ogl'), 'stats', 'dex'),
            'CON': pdf_get(self.character.spec('ogl'), 'stats', 'con'),
            'INT': pdf_get(self.character.spec('ogl'), 'stats', 'int'),
            'WIS': pdf_get(self.character.spec('ogl'), 'stats', 'wis'),
            'CHA': pdf_get(self.character.spec('ogl'), 'stats', 'cha'),
            'STRmod': self.character.spec('ogl').str_m(),
            'DEXmod': self.character.spec('ogl').dex_m(),
            'CONmod': self.character.spec('ogl').con_m(),
            'INTmod': self.character.spec('ogl').int_m(),
            'WISmod': self.character.spec('ogl').wis_m(),
            'CHamod': self.character.spec('ogl').cha_m(),
            'Passive': self.character.spec('dnd5e').passive_perception(),  # Passive Perception
            # Money:
            'CP': pdf_get(self.character.spec('ogl'), 'money', 'cp'),
            'SP': pdf_get(self.character.spec('ogl'), 'money', 'sp'),
            'GP': pdf_get(self.character.spec('ogl'), 'money', 'gp'),
            'Equipment': self._equipment(),
            'Features and Traits': self._features(),
            'Backstory': pdf_get(self.character.spec('general'), 'lore', 'backstory'),
            # Saves:
            'ST Strength': self.character.spec('dnd5e').save_bonus('str'), 'Check Box 11': self.character.spec('dnd5e')['proficiencies']['saves']['str'],
            'ST Dexterity': self.character.spec('dnd5e').save_bonus('dex'), 'Check Box 18': self.character.spec('dnd5e')['proficiencies']['saves']['dex'],
            'ST Constitution': self.character.spec('dnd5e').save_bonus('con'), 'Check Box 19': self.character.spec('dnd5e')['proficiencies']['saves']['con'],
            'ST Intelligence': self.character.spec('dnd5e').save_bonus('int'), 'Check Box 20': self.character.spec('dnd5e')['proficiencies']['saves']['int'],
            'ST Wisdom': self.character.spec('dnd5e').save_bonus('wis'), 'Check Box 21': self.character.spec('dnd5e')['proficiencies']['saves']['wis'],
            'ST Charisma': self.character.spec('dnd5e').save_bonus('cha'), 'Check Box 22': self.character.spec('dnd5e')['proficiencies']['saves']['cha'],
            # Skills:
            'Acrobatics': self.character.spec('dnd5e').skill_bonus('Acrobatics'), 'Check Box 23': self.character.spec('dnd5e')['skills']['Acrobatics']['proficiency'],
            'Animal': self.character.spec('dnd5e').skill_bonus('Animal Handling'), 'Check Box 24': self.character.spec('dnd5e')['skills']['Animal Handling']['proficiency'],  # Animal Handling
            'Arcana': self.character.spec('dnd5e').skill_bonus('Arcana'), 'Check Box 25': self.character.spec('dnd5e')['skills']['Arcana']['proficiency'],
            'Athletics': self.character.spec('dnd5e').skill_bonus('Athletics'), 'Check Box 26': self.character.spec('dnd5e')['skills']['Athletics']['proficiency'],
            'Deception': self.character.spec('dnd5e').skill_bonus('Deception'), 'Check Box 27': self.character.spec('dnd5e')['skills']['Deception']['proficiency'],
            'History': self.character.spec('dnd5e').skill_bonus('History'), 'Check Box 28': self.character.spec('dnd5e')['skills']['History']['proficiency'],
            'Insight': self.character.spec('dnd5e').skill_bonus('Insight'), 'Check Box 29': self.character.spec('dnd5e')['skills']['Insight']['proficiency'],
            'Intimidation': self.character.spec('dnd5e').skill_bonus('Intimidation'), 'Check Box 30': self.character.spec('dnd5e')['skills']['Intimidation']['proficiency'],
            'Investigation': self.character.spec('dnd5e').skill_bonus('Investigation'), 'Check Box 31': self.character.spec('dnd5e')['skills']['Investigation']['proficiency'],
            'Medicine': self.character.spec('dnd5e').skill_bonus('Medicine'), 'Check Box 32': self.character.spec('dnd5e')['skills']['Medicine']['proficiency'],
            'Nature': self.character.spec('dnd5e').skill_bonus('Nature'), 'Check Box 33': self.character.spec('dnd5e')['skills']['Nature']['proficiency'],
            'Perception': self.character.spec('dnd5e').skill_bonus('Perception'), 'Check Box 34': self.character.spec('dnd5e')['skills']['Perception']['proficiency'],
            'Performance': self.character.spec('dnd5e').skill_bonus('Performance'), 'Check Box 35': self.character.spec('dnd5e')['skills']['Performance']['proficiency'],
            'Persuasion': self.character.spec('dnd5e').skill_bonus('Persuasion'), 'Check Box 36': self.character.spec('dnd5e')['skills']['Persuasion']['proficiency'],
            'Religion': self.character.spec('dnd5e').skill_bonus('Religion'), 'Check Box 37': self.character.spec('dnd5e')['skills']['Religion']['proficiency'],
            'SleightofHand': self.character.spec('dnd5e').skill_bonus('Sleight of Hand'), 'Check Box 38': self.character.spec('dnd5e')['skills']['Sleight of Hand']['proficiency'],
            'Stealth': self.character.spec('dnd5e').skill_bonus('Stealth'), 'Check Box 39': self.character.spec('dnd5e')['skills']['Stealth']['proficiency'],
            'Survival': self.character.spec('dnd5e').skill_bonus('Survival'), 'Check Box 40': self.character.spec('dnd5e')['skills']['Survival']['proficiency'],
            # Weapons
            'Wpn Name': weapon_data[0]['name'],
            'Wpn1 AtkBonus': weapon_data[0]['atk_bonus'],
            'Wpn1 Damage': weapon_data[0]['damage'],
            'Wpn Name 2': weapon_data[1]['name'],
            'Wpn2 AtkBonus': weapon_data[1]['atk_bonus'],
            'Wpn2 Damage': weapon_data[1]['damage'],
            'Wpn Name 3': weapon_data[2]['name'],
            'Wpn3 AtkBonus': weapon_data[2]['atk_bonus'],
            'Wpn3 Damage': weapon_data[2]['damage'],
            'AttacksSpellcasting': weapon_data[3],
            'ProficienciesLang': self._profs()
        }

    def process(self) -> bytes:
        return process_pdf_form_fields(
            os.path.join(os.path.dirname(__file__), '..', '..', 'web', 'static', 'base_pdfs', 'dnd5e.pdf'),
            self._process_field
        )

    def _process_field(self, field: str) -> Union[str, bool, None]:
        return self.mapping[field] if field in self.mapping else None

    def _weapons(self):
        d = [
            {'name': '', 'atk_bonus': '', 'damage': ''},
            {'name': '', 'atk_bonus': '', 'damage': ''},
            {'name': '', 'atk_bonus': '', 'damage': ''},
            'Extra Weapons:\n',
        ]
        for i, weapon in enumerate(self.character.spec('dnd5e')['weapons'][:3]):
            d[i] = {
                'name': weapon['name'],
                'atk_bonus': weapon.to_hit(),
                'damage': weapon.damage(),
            }
        for weapon in self.character.spec('dnd5e')['weapons'][3:]:
            d[3] += f'{weapon["name"]} (hit: {weapon.to_hit()}, dmg: {weapon.damage()}), '
        d[3].rstrip(', ')
        return d

    def _features(self):
        abilities = self.character.spec('ogl')['class_abilities'] + \
                    self.character.spec('ogl')['race_abilities'] + \
                    self.character.spec('ogl')['extra_abilities']
        return ', '.join([a.split(':')[0] for a in abilities])

    def _equipment(self):
        it = ''
        for item in self.character.spec('ogl')['inventory']['on_hand']:
            count = 1
            if 'count' in item:
                count = item['count']
            it += f'{count}x {item["name"]}, '
        return it.rstrip(', ')

    def _profs(self):
        return f"""Weapon: {self.character.spec('dnd5e').weapon_proficiencies()}
Armor: {self.character.spec('dnd5e').armor_proficiencies()}
Tools: {self.character.spec('dnd5e').tool_proficiencies()}"""
