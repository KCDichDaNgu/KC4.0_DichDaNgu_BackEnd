from enum import Enum

class ExtendedEnum(Enum):

    @classmethod
    def enum_keys(cls):
        return list(map(lambda c: c.name, cls))
        
    @classmethod
    def enum_values(cls):
        return list(map(lambda c: c.value, cls))
