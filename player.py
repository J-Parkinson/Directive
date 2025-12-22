from typing import List
from card import GameCard
from Tiles.tile import Tile


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[GameCard] = []
        self.program: List[GameCard] = []  # The Stack
        self.owned_tiles: List[Tile] = []
        self.score: int = 0
