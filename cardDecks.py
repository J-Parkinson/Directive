from typing import List, Optional
from card import GameCard
from pile import Pile

class CardDecks:
    def __init__(self, all_cards: List[GameCard]):
        # The Draw Pile
        self.draw_pile = Pile[GameCard](all_cards).shuffle()

        # The Discard Pile (Starts empty)
        self.discard_pile = Pile[GameCard]([])

    @property
    def remaining(self) -> int:
        return len(self.draw_pile.items)

    def draw(self, count: int = 1) -> List[GameCard]:
        """
        Draws 'count' cards. Automatically handles reshuffling if the
        draw pile runs out mid-draw.
        """
        drawn_cards = []

        for _ in range(count):
            card = self.draw_one()
            if card:
                drawn_cards.append(card)
            else:
                # If None is returned even after reshuffle attempt, deck is truly empty
                break

        return drawn_cards

    def draw_one(self) -> Optional[GameCard]:
        """
        Draws a single card. Triggers reshuffle if empty.
        """
        if not self.draw_pile.items:
            self._reshuffle_discard_into_draw()

        # If still empty after reshuffle attempt, we are out of cards
        if not self.draw_pile.items:
            print("⚠️ SYSTEM ALERT: Memory Buffer Empty (No cards left).")
            return None

        # Helper returns a list, we take the first item
        result = self.draw_pile.draw(1)
        return result[0] if result else None

    def discard(self, cards: List[GameCard]):
        """Moves a list of cards to the discard pile."""
        if not cards:
            return
        self.discard_pile.add_to_top(cards)

    def discard_one(self, card: GameCard):
        """Moves a single card to the discard pile."""
        self.discard_pile.add_to_top([card])

    def _reshuffle_discard_into_draw(self):
        """
        The 'Cycle' Mechanic:
        Takes discard, shuffles it, becomes the new draw pile.
        """
        if not self.discard_pile.items:
            return  # Nothing to recycle

        print("🔄 RECYCLING MEMORY... (Reshuffling Discard to Draw)")

        # Move items over
        recyclable = self.discard_pile.draw(len(self.discard_pile.items))
        self.draw_pile.add_to_bottom(recyclable)

        # Shuffle the new main deck
        self.draw_pile.shuffle()

    def get_state(self):
        """Diagnostic helper."""
        return {
            "draw_count": len(self.draw_pile.items),
            "discard_count": len(self.discard_pile.items)
        }