import turtle
import math
from typing import Tuple, Optional


class Bounds(object):
    """
    A context manager for Line Clipping, relying on fast drawing.
    - All movement updates the actual turtle's position (unclamped).
    - Only the visible segments are drawn, using the color set by the user.
    - Stores only the minimal state needed for patching and teardown.
    """

    def __init__(self, xHeight: float, yHeight: float):
        """Initializes the bounds centered on (0,0)."""
        self.xMin = -xHeight / 2
        self.xMax = xHeight / 2
        self.yMin = -yHeight / 2
        self.yMax = yHeight / 2

        # --- MINIMAL STATE TRACKING ---
        self._original_forward = None
        self._original_goto = None
        self._original_fd = None
        self._original_setposition = None
        self._original_setpos = None
        self._original_setheading = None
        self._original_pencolor = None  # Stored for restoration in __exit__
        self._original_penstate = False
        self._original_pendown = None
        self._original_penup = None
        self._original_draw_bounding_box = None

    # --- Helper Methods ---

    def _liang_barsky_clip(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> Optional[
        Tuple[Tuple[float, float], Tuple[float, float]]]:
        """
        Implements the Liang-Barsky line clipping algorithm.
        Returns the clipped line segment (p1', p2') if visible, or None.
        """
        # (Implementation unchanged)
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1

        p = [-dx, dx, -dy, dy]
        q = [x1 - self.xMin, self.xMax - x1, y1 - self.yMin, self.yMax - y1]

        u1 = 0.0
        u2 = 1.0

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return None
            else:
                u = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u, u1)
                elif p[i] > 0:
                    u2 = min(u, u2)

        if u1 >= u2:
            return None

        clipped_x1 = x1 + u1 * dx
        clipped_y1 = y1 + u1 * dy
        clipped_x2 = x1 + u2 * dx
        clipped_y2 = y1 + u2 * dy

        return ((clipped_x1, clipped_y1), (clipped_x2, clipped_y2))

    def _draw_clipped_segment(self, new_true_pos: Tuple[float, float], old_true_pos: Tuple[float, float]):
        """
        Draws the clipped segment using the current user-specified color and
        then teleports the actual turtle to the new_true_pos to maintain path continuity.
        """
        is_pen_down = turtle.isdown()
        current_pencolor = turtle.pencolor()

        clipped_segment = self._liang_barsky_clip(old_true_pos, new_true_pos)

        # 1. Draw the segment if visible and pen is down
        if clipped_segment and is_pen_down:
            p_start, p_end = clipped_segment

            self._original_penup()
            self._original_goto(p_start)

            # Draw using the color currently set by the user (current_pencolor)
            self._original_pendown()
            # turtle.pencolor(current_pencolor) -- This is already the current color!
            self._original_goto(p_end)

            # Lift pen immediately
            self._original_penup()

        # 2. Teleport the actual turtle to the new *unclamped* position
        self._original_penup()
        self._original_goto(new_true_pos)

        # 3. Restore the user's intended pen state on the actual turtle
        if is_pen_down:
            self._original_pendown()
        # Note: If the user's pen was up, it remains up from the teleport.

    # --- Bounded Movement Methods ---

    def _bounded_forward(self, distance: float):
        old_true_pos = turtle.pos()
        heading = turtle.heading()

        new_true_x = old_true_pos[0] + distance * math.cos(math.radians(heading))
        new_true_y = old_true_pos[1] + distance * math.sin(math.radians(heading))
        new_true_pos = (new_true_x, new_true_y)

        self._draw_clipped_segment(new_true_pos, old_true_pos)

    def _bounded_back(self, distance: float):
        turtle.left(180)
        self._bounded_forward(distance)
        turtle.left(180)

    def _bounded_goto(self, x: float, y: float = None):
        if isinstance(x, tuple) and y is None:
            x, y = x
        elif y is None:
            raise ValueError("goto requires both x and y coordinates or a tuple.")

        old_true_pos = turtle.pos()
        new_true_pos = (x, y)

        self._draw_clipped_segment(new_true_pos, old_true_pos)

    def _bounded_circle(self, radius: float, extent: Optional[float] = None, steps: Optional[int] = None):
        """
        Custom 'circle' method that breaks the arc into small segments and
        calls the patched forward method for clipping.
        """
        if extent is None:
            extent = 360.0

        if steps is None:
            # Use a fixed number of steps per 360 degrees, scaling for the extent
            steps = int(abs(extent) / 360.0 * 180)
            steps = max(steps, 1)  # Ensure at least one step

        # Calculate the distance and angle for each segment
        arc_length = 2 * math.pi * abs(radius) * (abs(extent) / 360.0)
        segment_length = arc_length / steps
        segment_angle = extent / steps

        # Determine if turning left or right (based on sign of radius)
        turn_func = turtle.left if radius > 0 else turtle.right

        turn_func(segment_angle/2)

        # Execute the arc segment by segment
        for _ in range(steps):
            # The patched forward method handles the clipped drawing
            self._bounded_forward(segment_length)

            # The actual turn is executed using the unpatched method
            # This updates turtle.heading() correctly for the next forward calculation
            turn_func(segment_angle)

        turn_func(-segment_angle/2)

    # --- Bounding Box Method ---

    def _bounding_box(self, radius: float = 0):
        """Draws the bounding box with optional rounded corners defined by 'radius'."""
        radius = max(0, radius)

        # --- State Backup ---
        isPenDown = turtle.isdown()
        originalLocation = turtle.pos()
        originalHeading = turtle.heading()

        # Calculate bounding box dimensions
        height = self.yMax - self.yMin
        width = self.xMax - self.xMin
        boundingHeight = height - (radius * 2)
        boundingWidth = width - (radius * 2)

        if min(boundingHeight, boundingWidth) < 0:
            raise Exception("Radius too large")

        # --- Setup for Drawing ---
        self._original_penup()
        # 1. Move to the starting point (bottom-left start)
        self._original_goto(self.xMin + radius, self.yMin)
        self._original_pendown()

        # Draw the box using original methods
        self._original_setheading(0)  # Start East

        for _ in range(2):
            self._original_forward(boundingWidth)
            turtle.circle(radius, 90)
            self._original_forward(boundingHeight)
            turtle.circle(radius, 90)

        # --- State Restoration ---
        self._original_penup()

        # Restore position, heading, color, and pensize
        self._original_goto(originalLocation)
        self._original_setheading(originalHeading)

        # Restore pen state
        if isPenDown:
            self._original_pendown()

    # --- Context Manager Methods ---

    def __enter__(self):
        """Setup: Saves original methods, patches movement, and saves state."""
        # Save original methods and state
        self._original_forward = turtle.forward
        self._original_fd = turtle.fd
        self._original_goto = turtle.goto
        self._original_backward = turtle.backward
        self._original_back = turtle.back
        self._original_bk = turtle.bk
        self._original_setposition = turtle.setposition
        self._original_setpos = turtle.setpos
        self._original_setheading = turtle.setheading
        self._original_pendown = turtle.pendown
        self._original_penup = turtle.penup
        self._original_circle = turtle.circle

        self._original_pencolor = turtle.pencolor()
        self._original_penstate = turtle.isdown()

        # Monkey-patch Movement
        turtle.forward = self._bounded_forward
        turtle.fd = self._bounded_forward
        turtle.backward = self._bounded_back
        turtle.back = self._bounded_back
        turtle.bk = self._bounded_back
        turtle.goto = self._bounded_goto
        turtle.setpos = self._bounded_goto
        turtle.setposition = self._bounded_goto
        turtle.circle = self._bounded_circle

        # Save and patch boundingbox method
        self._original_draw_bounding_box = getattr(turtle.Turtle, 'boundingbox', None)
        turtle.Turtle.boundingbox = self._bounding_box

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Teardown: Restores the original Turtle methods and original state."""
        # Restore original movement methods
        turtle.forward = self._original_forward
        turtle.fd = self._original_fd
        turtle.backward = self._original_backward
        turtle.back = self._original_back
        turtle.bk = self._original_bk
        turtle.goto = self._original_goto
        turtle.setpos = self._original_setpos
        turtle.setposition = self._original_setposition
        turtle.circle = self._original_circle

        # Restore boundingbox method
        if self._original_draw_bounding_box is None:
            if hasattr(turtle.Turtle, 'boundingbox'):
                del turtle.Turtle.boundingbox
        else:
            turtle.Turtle.boundingbox = self._original_draw_bounding_box

        # Restore final state
        turtle.pencolor(self._original_pencolor)

        # The final position and heading are already correct from the last teleport
        if self._original_penstate:
            self._original_pendown()
        else:
            self._original_penup()

        return False