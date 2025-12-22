from enum import Enum

class Direction(Enum):
    Up = 0
    Left = 1
    Down = 2
    Right = 3

    def rotate(self, clockwise: bool):
        return Orientation((self.value + 1 if clockwise else self.value - 1) % 4)

class Orientation(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

    def rotate(self, clockwise: bool):
        return Orientation((self.value + 1 if clockwise else self.value - 1) % 4)
