from typing import List, Type, Any

from Tiles.flipTile import FlipTile
from Tiles.tile import Tile, AsymmetricTile
from Tiles.tiles import (
    ReverseTile, MergeTile, QuadMergeTile, ForkTile,
    TurnTile, CrossroadsTile, DivergeTile, DivergeMergeTile
)
from direction import Direction, Orientation
from pile import Pile


class TilePile(Pile[Tile]):
    """Strictly typed pile for Hardware Tiles."""

    def __init__(self, items: List[Tile] = None):
        super().__init__(items or [])


def generate_tile_pile() -> TilePile:
    items: List[Tile] = []

    def add_tile(cls: Type[Tile], **kwargs: Any):
        """
        Creates a concrete tile instance.
        If it's an AsymmetricTile, alternates wrapping it in a FlipTile.
        """
        t = cls(None, Orientation.North, **kwargs)

        # Check if this specific tile class inherits from AsymmetricTile
        if isinstance(t, AsymmetricTile) and len(items) % 2 == 1:
            items.append(FlipTile(t))
        else:
            items.append(t)

    # 1. Reverse (10) - Symmetrical
    for _ in range(10): add_tile(ReverseTile)

    # 2. Merge (20) - Asymmetric (Choice: Left vs Right)
    for _ in range(10): add_tile(MergeTile, default_choice=Direction.Left)
    for _ in range(10): add_tile(MergeTile, default_choice=Direction.Right)

    # 3. QuadMerge (20) - Asymmetric
    quad_choices = [Direction.Left, Direction.Right, Direction.Down]
    for i in range(20): add_tile(QuadMergeTile, default_choice=quad_choices[i % 3])

    # 4. Fork (20) - Asymmetric (Physical 'r' vs 'l')
    for _ in range(10): add_tile(ForkTile, default_choice=Direction.Up)
    for _ in range(10): add_tile(ForkTile, default_choice=Direction.Right)

    # 5. Turn (8) - Asymmetric (Physical 'r' vs 'l' curve)
    for _ in range(8): add_tile(TurnTile)

    # 6. Crossroads (4) - Symmetrical
    for _ in range(4): add_tile(CrossroadsTile)

    # 7. Diverge (8) - Asymmetric
    for _ in range(8): add_tile(DivergeTile)

    # 8. Diverge Merge (4) - Asymmetric
    for _ in range(2): add_tile(DivergeMergeTile, default_side=Direction.Left)
    for _ in range(2): add_tile(DivergeMergeTile, default_side=Direction.Right)

    return TilePile(items)