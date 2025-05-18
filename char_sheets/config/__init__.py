import os

from char_sheets.config.characters import Characters


def load_config() -> Characters:
    doc = Characters.from_yaml(os.path.abspath(os.path.join('characters', 'chars.yml')))
    doc.resolve_and_merge_references([os.path.abspath(os.path.join('characters', 'base'))])
    doc.process_vars()
    doc.validate()
    doc.freeze()
    return doc['characters']
