from typing import Dict, List, Optional
from direction import Direction, Orientation
from player import Player


class Tile:
    def __init__(self, x: int, y: int, orientation: Orientation, ownership: Player = None):
        self.coords = (x, y)
        self.orientation = orientation  # Current rotation state
        self.ownership = ownership

        # These represent the "Factory Default" (North) layout
        self._base_paths: Dict[Direction, List[Direction]] = {}
        self._base_defaults: Dict[Direction, Optional[Direction]] = {}

    def rotate(self, clockwise: bool = True):
        """Rotates the tile 90 degrees."""
        self.orientation = self.orientation.rotate(clockwise)

    def _transform_dir(self, d: Direction, reverse: bool = False) -> Direction:
        """
        Adjusts a direction based on the current orientation.
        If reverse=True, maps world-space direction back to local tile-space.
        """
        # This assumes Direction and Orientation share an underlying numeric value
        # (e.g., North=0, East=1, South=2, West=3)
        shift = self.orientation.value
        if reverse:
            return Direction((d.value - shift) % 4)
        return Direction((d.value + shift) % 4)

    @property
    def paths(self) -> Dict[Direction, List[Direction]]:
        """World-space mapping of entries to exits."""
        rotated_paths = {}
        for entry, exits in self._base_paths.items():
            world_entry = self._transform_dir(entry)
            world_exits = [self._transform_dir(ex) for ex in exits]
            rotated_paths[world_entry] = world_exits
        return rotated_paths

    @property
    def defaultPaths(self) -> Dict[Direction, Optional[Direction]]:
        """World-space mapping of default exits."""
        rotated_defaults = {}
        for entry, exit_dir in self._base_defaults.items():
            world_entry = self._transform_dir(entry)
            world_exit = self._transform_dir(exit_dir) if exit_dir else None
            rotated_defaults[world_entry] = world_exit
        return rotated_defaults

    # --- Interaction Methods ---

    def can_enter(self, from_dir: Direction) -> bool:
        return from_dir in self.paths

    def get_options(self, from_dir: Direction) -> List[Direction]:
        return self.paths.get(from_dir, [])

    def get_exit(self, from_dir: Direction) -> Optional[Direction]:
        options = self.get_options(from_dir)
        if not options:
            return None
        if len(options) == 1:
            return options[0]
        return self.defaultPaths.get(from_dir)
