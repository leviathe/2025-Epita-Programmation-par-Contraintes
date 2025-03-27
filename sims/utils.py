from enum import Enum, IntEnum

class Tile(IntEnum):
    NONE = 0
    ROAD = 1
    WATER = 2
    HOUSE = 3

class StringEnum(str, Enum):
    def __str__(self):
        return self.value