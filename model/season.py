from enum import Enum


class Season(Enum):
    SEASON_2023_2024 = "2023-2024"
    SEASON_2024_2025 = "2024-2025"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
