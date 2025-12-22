from dataclasses import dataclass
from game import DirectiveGame
from hydrate import HydratedCard

@dataclass
class GameCard:
    """
    Runtime wrapper for HydratedCard data. 
    Handles the execution of the 16-bit logic strings.
    """
    data: HydratedCard

    def __post_init__(self):
        # Shortcut attributes for easy access
        self.id = self.data.id
        self.title = self.data.title
        self.color = self.data.color

        # We pre-compile the lambdas if possible, or store strings
        # Storing strings is safer for serialization if needed later
        self._exec_code = self.data.execute['function']
        self._write_code = self.data.write['function']
        self._delete_code = self.data.delete['function']

    def print(self):
        """16-bit terminal visualization."""
        c_map = {"Blue": "34", "Yellow": "33", "Red": "31", "Green": "32"}
        ansi = c_map.get(self.color, "37")  # Default white

        border = "═" * 30
        print(f"\033[{ansi}m╔{border}╗")
        print(f"║ {self.title.center(28)} ║")
        print(f"║ {self.id.ljust(28)} ║")
        print(f"╠{'─' * 30}╣")
        print(f"║ E: {self.data.execute['text'][:25].ljust(25)} ║")
        print(f"║ W: {self.data.write['text'][:25].ljust(25)} ║")
        print(f"╚{border}╝\033[0m")

    def _run_logic(self, logic_str: str, game_state: DirectiveGame):
        """
        Executes the lambda string with the game state injected as 'g'.
        """
        context = {'g': game_state}
        try:
            # Evaluate the string to get the function, then call it with game_state
            # Assuming format: "lambda g: g.do_something()"
            action_func = eval(logic_str, {"__builtins__": None}, context)
            return action_func(game_state)
        except Exception as e:
            print(f"⚠️ RUNTIME ERROR [{self.id}]: {e}")
            return None

    def execute(self, game: DirectiveGame):
        return self._run_logic(self._exec_code, game)

    def write(self, game: DirectiveGame):
        return self._run_logic(self._write_code, game)

    def delete(self, game: DirectiveGame):
        return self._run_logic(self._delete_code, game)