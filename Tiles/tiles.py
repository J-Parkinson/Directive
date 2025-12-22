from typing import Optional

from Tiles.tile import Tile, AsymmetricTile
from board import Coord
from direction import Direction, Orientation


class StartTile(Tile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation):
        super().__init__(coord, orientation)
        self._base_paths = {Direction.Up: [Direction.Up]}
        # No choice possible, no defaults needed.


class ReverseTile(Tile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation):
        super().__init__(coord, orientation)
        # Assuming Reverse bounces from all sides back to themselves
        self._base_paths = {
            Direction.Up: [Direction.Up],
            Direction.Down: [Direction.Down],
            Direction.Left: [Direction.Left],
            Direction.Right: [Direction.Right]
        }
        # Every entry has exactly one exit.


class MergeTile(Tile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation, default_choice: Direction):
        super().__init__(coord, orientation)
        self._base_paths = {
            Direction.Left: [Direction.Up],
            Direction.Right: [Direction.Up],
            Direction.Up: [Direction.Left, Direction.Right]
        }
        # Choice only exists when entering from the "Output" (Up)
        self._base_defaults = {Direction.Up: default_choice}


class QuadMergeTile(Tile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation, default_choice: Direction):
        super().__init__(coord, orientation)
        self._base_paths = {
            Direction.Left: [Direction.Up],
            Direction.Right: [Direction.Up],
            Direction.Down: [Direction.Up],
            Direction.Up: [Direction.Left, Direction.Right, Direction.Down]
        }
        # Choice only exists when entering from the "Output" (Up)
        self._base_defaults = {Direction.Up: default_choice}


class ForkTile(AsymmetricTile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation, default_choice: Direction):
        super().__init__(coord, orientation)
        self._base_paths = {
            Direction.Down: [Direction.Up, Direction.Right],
            Direction.Up: [Direction.Down],
            Direction.Right: [Direction.Down]
        }
        # Choice only exists when entering from the "Stem" (Down)
        self._base_defaults = {Direction.Down: default_choice}


class TurnTile(AsymmetricTile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation):
        super().__init__(coord, orientation)
        self._base_paths = {
            Direction.Down: [Direction.Right],
            Direction.Right: [Direction.Down]
        }
        # Deterministic.


class CrossroadsTile(Tile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation):
        super().__init__(coord, orientation)
        self._base_paths = {
            Direction.Up: [Direction.Down],
            Direction.Down: [Direction.Up],
            Direction.Left: [Direction.Right],
            Direction.Right: [Direction.Left]
        }
        # Deterministic.


class DivergeTile(Tile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation):
        super().__init__(coord, orientation)
        self._base_paths = {
            Direction.Down: [Direction.Right],
            Direction.Right: [Direction.Down],
            Direction.Up: [Direction.Left],
            Direction.Left: [Direction.Up]
        }
        # Deterministic.


class DivergeMergeTile(Tile):
    def __init__(self, coord: Optional[Coord], orientation: Orientation, default_side: Direction):
        super().__init__(coord, orientation)
        self._base_paths = {
            Direction.Up: [Direction.Left, Direction.Right],
            Direction.Right: [Direction.Down, Direction.Up],
            Direction.Down: [Direction.Left, Direction.Right],
            Direction.Left: [Direction.Up, Direction.Down]
        }

        # As requested: Diverge Merge defaults are "All Left" or "All Right"
        # based on the relative entry.
        if default_side == Direction.Left:
            self._base_defaults = {
                Direction.Up: Direction.Left,
                Direction.Right: Direction.Up,
                Direction.Down: Direction.Right,
                Direction.Left: Direction.Down
            }
        else:  # default_side == Direction.Right
            self._base_defaults = {
                Direction.Up: Direction.Right,
                Direction.Right: Direction.Down,
                Direction.Down: Direction.Left,
                Direction.Left: Direction.Up
            }