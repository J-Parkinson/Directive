from game import DirectiveGame
from hydrate import HydratedCard
from dataclasses import dataclass
from pile import Pile

@dataclass
class GameCard:
    def __init__(self, data: HydratedCard):
        self.data = data
        self.id = data.id
        self.title = data.title
        self.color = data.color
        self.execute_logic = data.execute['function']
        self.write_logic = data.write['function']
        self.delete_logic = data.delete['function']

    def print(self):
        """Pretty prints the card in a terminal/16-bit style."""
        border = "═" * 30
        print(f"╔{border}╗")
        print(f"║ {self.title.ljust(28)} ║")
        print(f"║ ID: {self.id.ljust(26)} ║")
        print(f"╠{'═' * 30}╣")
        print(f"║ EXEC: {self.data.execute['text'][:24]}... ║")
        print(f"║ WRITE: {self.data.write['text'][:23]}... ║")
        print(f"╚{border}╝")

    def _run_logic(self, logic_str: str, game: DirectiveGame):
        """Safely evaluates the lambda logic against the game state."""
        try:
            # We pass the game object as 'g' to match our lambda definitions
            logic_func = eval(logic_str)
            return logic_func(game)
        except Exception as e:
            print(f"CRITICAL ERROR in {self.id} logic: {e}")
            return game

    def execute(self, game: DirectiveGame):
        return self._run_logic(self.execute_logic, game)

    def write(self, game: DirectiveGame):
        return self._run_logic(self.write_logic, game)

    def delete(self, game: DirectiveGame):
        return self._run_logic(self.delete_logic, game)

MainDeck = Pile[GameCard]
DiscardDeck = Pile[GameCard]