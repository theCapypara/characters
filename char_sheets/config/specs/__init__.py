from abc import ABC

from configcrunch import YamlConfigDocument


class AbstractSpec(YamlConfigDocument, ABC):
    pass
