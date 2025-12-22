from typing import List, Tuple, Dict, Optional, Set
from Tiles.tile import Tile
from Tiles.tiles import StartTile
from direction import Orientation

# Type alias for cleaner signatures
Coord = Tuple[int, int]

class GameBoard:
    def __init__(self, max_radius: int = 3):
        """
        max_radius: Limits the board size. 3 implies a 7x7 grid (Center + 3 in each dir).
        """
        self.max_radius = max_radius

        # The central source of truth
        self.grid: Dict[Coord, Tile] = {
            (0, 0): StartTile((0, 0), Orientation.North)
        }

        # Optimization: Track empty spots adjacent to placed tiles
        # This makes the UI much faster (don't have to scan the whole grid)
        self.valid_slots: Set[Coord] = set(self._get_all_neighbors((0, 0)))

    def is_valid_location(self, coords: Coord) -> bool:
        """
        Standard Rule:
        1. Spot must be empty.
        2. Spot must be within grid boundaries.
        3. Spot must be adjacent to an existing tile.
        """
        x, y = coords

        # 1. Occupied check
        if coords in self.grid:
            return False

        # 2. Boundary check (Simple Square Box)
        if abs(x) > self.max_radius or abs(y) > self.max_radius:
            return False

        # 3. Adjacency check
        # We check if this coord is in our pre-calculated 'frontier' set
        return coords in self.valid_slots

    def place_tile(self, tile: Tile, coords: Coord, force: bool = False):
        """
        The main state-change method.
        force: If True (e.g. via Red Card), bypasses validation.
        """
        if not force and not self.is_valid_location(coords):
            raise ValueError(f"Invalid placement at {coords}")

        # 1. Update Tile State
        tile.coords = coords

        # 2. Update Grid State
        self.grid[coords] = tile

        # 3. Update 'Frontier' (Valid Slots)
        # Remove the spot we just filled
        if coords in self.valid_slots:
            self.valid_slots.remove(coords)

        # Add new empty neighbors to the frontier
        for n_coord in self._get_all_neighbors(coords):
            if n_coord not in self.grid and self._is_within_bounds(n_coord):
                self.valid_slots.add(n_coord)

    # --- Helpers ---

    def _is_within_bounds(self, coords: Coord) -> bool:
        x, y = coords
        return abs(x) <= self.max_radius and abs(y) <= self.max_radius

    def _get_all_neighbors(self, coords: Coord) -> List[Coord]:
        """Returns coordinates of North, South, East, West neighbors."""
        x, y = coords
        # Mapping Direction to coordinate offsets could be centralized
        return [
            (x, y + 1),  # Up (North)
            (x, y - 1),  # Down (South)
            (x + 1, y),  # Right (East)
            (x - 1, y)  # Left (West)
        ]

    def get_tile_at(self, coords: Coord) -> Optional[Tile]:
        """Safe getter."""
        return self.grid.get(coords)