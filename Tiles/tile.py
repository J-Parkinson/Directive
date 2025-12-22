from typing import Dict, List, Optional

from board import Coord
from direction import Direction, Orientation
from player import Player

class Tile:
    def __init__(self, coord: Optional[Coord], orientation: Orientation, ownership: Player = None):
        self.coords = coord
        self.orientation = orientation
        self.ownership = ownership

        # Factory Default (Local Tile-space)
        self._base_paths: Dict[Direction, List[Direction]] = {}
        self._base_defaults: Dict[Direction, Optional[Direction]] = {}

    def rotate(self, clockwise: bool = True):
        """Modifies the tile's orientation in 90-degree increments."""
        current = self.orientation.value
        step = 1 if clockwise else -1
        self.orientation = Orientation((current + step) % 4)

    def _to_world(self, tile_dir: Direction) -> Direction:
        """Maps a local Tile Direction to a World Direction based on Orientation."""
        return Direction((tile_dir.value + self.orientation.value) % 4)

    def _to_tile(self, world_dir: Direction) -> Direction:
        """Maps a World Direction back to the Tile's local coordinate space."""
        return Direction((world_dir.value - self.orientation.value) % 4)

    @property
    def world_paths(self) -> Dict[Direction, List[Direction]]:
        """World-space mapping of entries to exits."""
        rotated = {}
        for local_entry, local_exits in self._base_paths.items():
            world_entry = self._to_world(local_entry)
            rotated[world_entry] = [self._to_world(ex) for ex in local_exits]
        return rotated

    @property
    def world_defaults(self) -> Dict[Direction, Optional[Direction]]:
        """World-space mapping of default automatic exits."""
        rotated = {}
        for local_entry, local_exit in self._base_defaults.items():
            world_entry = self._to_world(local_entry)
            world_exit = self._to_world(local_exit) if local_exit else None
            rotated[world_entry] = world_exit
        return rotated

    # --- Interaction Logic (The API for the Robot/Game) ---

    def can_enter(self, world_entry_dir: Direction) -> bool:
        """Checks if a robot approaching from a specific world direction can enter."""
        return world_entry_dir in self.world_paths

    def get_options(self, world_entry_dir: Direction) -> List[Direction]:
        """Returns all possible exit directions in world-space."""
        return self.world_paths.get(world_entry_dir, [])

    def get_exit(self, world_entry_dir: Direction) -> Optional[Direction]:
        """
        Determines the world-space exit.
        Returns Direction for auto-paths, or None if a manual Choice is required.
        """
        options = self.get_options(world_entry_dir)
        if not options:
            return None  # Wall collision

        if len(options) == 1:
            return options[0]

        return self.world_defaults.get(world_entry_dir)

AsymmetricTile = Tile