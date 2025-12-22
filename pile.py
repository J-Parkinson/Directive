from typing import TypeVar, Generic, List
import random

# Define a Type Variable 'T'.
# This acts as a placeholder that will be locked in when the class is created.
T = TypeVar('T')

class Pile(Generic[T]):
    def __init__(self, items: List[T] = []):
        # Now Python knows self.items is a list of a specific type, not just anything.
        self.items: List[T] = items
        self.shuffle()

    def shuffle(self) -> 'Pile[T]':
        random.shuffle(self.items)
        return self

    def draw(self, count: int = 1) -> List[T]:
        drawn = self.items[:count]
        self.items = self.items[count:]
        return drawn

    def add_to_bottom(self, items: List[T]) -> 'Pile[T]':
        self.items.extend(items)
        return self

    def add_to_top(self, items: List[T]) -> 'Pile[T]':
        self.items = [*items, *self.items]
        return self