from typing import Tuple

class Robot:
    def __init__(self, start_pos: Tuple[int, int]):
        self.battery: int = 10
        self.location: Tuple[int, int] = start_pos
        self.direction: str = "North"