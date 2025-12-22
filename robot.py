from typing import Tuple, List
from direction import Direction
from board import GameBoard, Coord


class Robot:
    def __init__(self, start_pos: Coord = (0, 0), start_facing: Direction = Direction.Up):
        # State
        self.battery: int = 10
        self.location: Coord = start_pos
        self.facing: Direction = start_facing

        # Diagnostics / Undo Support
        self.is_crashed: bool = False
        self.history: List[Coord] = [start_pos]

    def pay_battery(self, cost: int) -> bool:
        """
        Attempts to spend battery for an action (e.g. Manual Override).
        Returns True if successful, False if insufficient charge.
        """
        if self.battery >= cost:
            self.battery -= cost
            return True
        return False

    def damage(self, amount: int):
        """Reduces battery, potentially triggering a shutdown/reset."""
        self.battery = max(0, self.battery - amount)
        if self.battery == 0:
            self._trigger_system_reset()

    def move(self, board: GameBoard):
        """
        The main physics step.
        Calculates the next tile based on current facing and attempts to move.
        """
        if self.is_crashed or self.battery <= 0:
            return  # Robot is dead

        # 1. Calculate the coordinate we are moving INTO
        dx, dy = self._get_delta(self.facing)
        curr_x, curr_y = self.location
        next_pos = (curr_x + dx, curr_y + dy)

        # 2. Check if the Tile exists (Board Boundary / Void check)
        target_tile = board.get_tile_at(next_pos)

        if not target_tile:
            print(f"⚠️ CRASH: Robot moved off-board at {next_pos}")
            self._handle_crash()
            return

        # 3. Determine Entry Direction (Inverse of current facing)
        # If I am moving UP (North), I enter the tile from the DOWN (South) side.
        entry_side = self._inverse_direction(self.facing)

        # 4. Ask the Tile for the Exit
        # This triggers the Tile's internal logic (Default vs Manual Directive)
        exit_dir = target_tile.get_exit(entry_side)

        if exit_dir is None:
            print(f"⚠️ CRASH: Robot hit a wall at {next_pos}")
            self._handle_crash()
            return

        # 5. Success - Update State
        self.location = next_pos
        self.facing = exit_dir
        self.history.append(self.location)

        print(f"🤖 MOVED: {self.location} | Facing: {self.facing.name}")

    # --- Internal Helpers ---

    def _handle_crash(self):
        """
        Logic for when the robot fails navigation.
        Standard penalty: Lose battery, Reset to Start.
        """
        self.damage(2)  # Penalty cost
        self.is_crashed = True
        self._trigger_system_reset()

    def _trigger_system_reset(self):
        """Resets robot to the kernel (Start Tile)."""
        print("🔄 SYSTEM RESET INITIATED...")
        self.location = (0, 0)
        self.facing = Direction.Up
        self.is_crashed = False
        self.history.clear()

    def _get_delta(self, d: Direction) -> Tuple[int, int]:
        # Mapping Direction enum to Grid Math
        # Assuming: Up=0, Left=1, Down=2, Right=3 (Counter-Clockwise)
        if d == Direction.Up:    return (0, 1)
        if d == Direction.Left:  return (-1, 0)
        if d == Direction.Down:  return (0, -1)
        if d == Direction.Right: return (1, 0)
        return (0, 0)

    def _inverse_direction(self, d: Direction) -> Direction:
        # Returns the opposite side (e.g., Up -> Down)
        # (Value + 2) % 4 works for both Clockwise and Counter-Clockwise
        # as long as opposites are spaced by 2.
        return Direction((d.value + 2) % 4)