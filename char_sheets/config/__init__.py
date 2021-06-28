import os

from char_sheets.config.characters import Characters


def load_config() -> Characters:
    doc = Characters.from_yaml(os.path.join(os.path.dirname(__file__), 'chars.yml'))
    doc.resolve_and_merge_references([os.path.join(os.path.dirname(__file__), 'base')])
    doc.process_vars()
    doc.validate()
    return doc
