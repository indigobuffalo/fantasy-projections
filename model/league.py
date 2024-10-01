from enum import Enum


class League(Enum):
    ANY = 'any'
    KKUPFL = 'kkupfl'
    PUCKIN_AROUND = 'pa'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    __hash__ = Enum.__hash__ 
