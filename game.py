from typing import List
from board import GameBoard
from card import GameCard, MainDeck, DiscardDeck
from player import Player
from robot import Robot


class DirectiveGame:
    def __init__(self, cards: List[GameCard], noPlayers: int):
        self.board = GameBoard(5, 5)
        self.robot = Robot((2, 2))
        self.players = [Player(f"Player {str(i)}") for i in range(noPlayers)]
        self.main_deck = MainDeck(cards)
        self.discard_deck = DiscardDeck()
        self.current_player_idx = 0
        self.battery_max = 20

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_idx]

    def add_vp(self, amount: int):
        self.current_player.score += amount
        return self

    def add_battery(self, amount: int):
        self.robot.battery = min(self.battery_max, self.robot.battery + amount)
        return self

    def calculate_global_scores(self):
        """Computes final scoring based on board state."""
        for p in self.players:
            # Add bonus for tile count, etc.
            p.score += len(p.owned_tiles)
        return {p.name: p.score for p in self.players}