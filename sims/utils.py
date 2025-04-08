from enum import Enum, IntEnum

class Tile(IntEnum):
    NONE = 0
    ROAD = 1
    WATER = 2
    HOUSE = 3
    HOSPITAL = 4
    DAM = 5

class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class StringEnum(str, Enum):
    def __str__(self):
        return self.value