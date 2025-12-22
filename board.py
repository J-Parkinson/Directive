from typing import List, Tuple, Dict
from robot import Robot
from Tiles.tile import Tile

class GameBoard:
    def __init__(self):
        self.grid: Dict[Tuple[int, int], Tile] = {
            (0,0): Start
        }

    def navigate(self, robot: Robot, distance: int):
        """Logic for moving the robot across the grid."""
        # Simple implementation: move in robot's current direction
        x, y = robot.location
        # (Movement logic would go here based on tile exits)
        pass

    def get_neighbors(self, coords: Tuple[int, int]) -> List[Tile]:
        x, y = coords
        neighbor_coords = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
        return [self.grid[c] for c in neighbor_coords if c in self.grid]