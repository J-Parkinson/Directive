from typing import Optional

from Tiles.tile import Tile
from direction import Direction, Orientation

class StartTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation):
        super().__init__(x, y, orientation)
        self._base_paths = { Direction.Up: [Direction.Up] }

class ReverseTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation):
        super().__init__(x, y, orientation)
        self._base_paths = { Direction.Up: [Direction.Up] }

class MergeTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation, defaultPath: Optional[Direction]):
        super().__init__(x, y, orientation)
        self._base_paths = {
            Direction.Left: [Direction.Up],
            Direction.Right: [Direction.Up],
            Direction.Up: [Direction.Left, Direction.Right]
        }

class QuadMergeTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation, defaultPath: Optional[Direction]):
        super().__init__(x, y, orientation)
        self._base_paths = {
            Direction.Left: [Direction.Up],
            Direction.Right: [Direction.Up],
            Direction.Down: [Direction.Up],
            Direction.Up: [Direction.Left, Direction.Right, Direction.Down]
        }

class ForkTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation, defaultPath: Optional[Direction]):
        super().__init__(x, y, orientation)
        self._base_paths = {
            Direction.Down: [Direction.Up, Direction.Right],
            Direction.Up: [Direction.Down],
            Direction.Right: [Direction.Down]
        }

class TurnTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation):
        super().__init__(x, y, orientation)
        self._base_paths = {
            Direction.Down: [Direction.Right],
            Direction.Right: [Direction.Down]
        }

class CrossroadsTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation):
        super().__init__(x, y, orientation)
        self._base_paths = {
            Direction.Up: [Direction.Down],
            Direction.Down: [Direction.Up],
            Direction.Left: [Direction.Right],
            Direction.Right: [Direction.Left]
        }

class DivergeTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation):
        super().__init__(x, y, orientation)
        self._base_paths = {
            Direction.Down: [Direction.Right],
            Direction.Right: [Direction.Down],
            Direction.Up: [Direction.Left],
            Direction.Left: [Direction.Up]
        }

class DivergeMergeTile(Tile):
    def __init__(self, x: int, y: int, orientation: Orientation):
        super().__init__(x, y, orientation)
        self._base_paths = {
            Direction.Up: [Direction.Left, Direction.Right],
            Direction.Right: [Direction.Down, Direction.Up],
            Direction.Down: [Direction.Left, Direction.Right],
            Direction.Left: [Direction.Up, Direction.Down]
        }