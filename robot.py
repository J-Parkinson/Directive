from board import Coord

class Robot:
    def __init__(self, start_pos: Coord):
        self.battery: int = 10
        self.location: Coord = start_pos
        self.direction: str = "North"