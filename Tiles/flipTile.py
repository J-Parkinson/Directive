from Tiles.tile import Tile
from direction import Direction

class FlipTile(Tile):
    """
    A decorator/wrapper that mirrors a Tile's internal geometry.
    """
    def __init__(self, wrapped_tile: Tile):
        # We pass the wrapped tile's current properties to the base Tile
        super().__init__(
            wrapped_tile.coords,
            wrapped_tile.orientation,
            wrapped_tile.ownership
        )
        self.wrapped_tile = wrapped_tile

    def _flip(self, d: Direction) -> Direction:
        """Horizontal swap: Left becomes Right, Right becomes Left."""
        if d == Direction.Left: return Direction.Right
        if d == Direction.Right: return Direction.Left
        return d

    # --- Overriding Transformation Logic ---
    # Because world_paths in the base Tile class calls self._to_world,
    # these overrides will automatically 'flip' the output of world_paths.

    def _to_world(self, tile_dir: Direction) -> Direction:
        # Flip the design first, then rotate it
        return super()._to_world(self._flip(tile_dir))

    def _to_tile(self, world_dir: Direction) -> Direction:
        # Un-rotate first, then un-flip
        return self._flip(super()._to_tile(world_dir))

    # --- Delegation ---
    # Ensure FlipTile looks at the wrapped tile's paths, not its own empty dicts.

    @property
    def _base_paths(self):
        return self.wrapped_tile._base_paths

    @property
    def _base_defaults(self):
        return self.wrapped_tile._base_defaults

    def __getattr__(self, name):
        """Pass any other attribute access (like current_directive) to the inner tile."""
        return getattr(self.wrapped_tile, name)