from enum import Enum


class ReaderKind(Enum):
    HISTORICAL = 'historical'
    PROJECTION = 'projection'
    SCHEDULE = 'schedule'

    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
