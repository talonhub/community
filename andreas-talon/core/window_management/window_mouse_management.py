from talon import ui, Module, actions
from talon.types import Rect
from dataclasses import dataclass

mod = Module()


@dataclass
class Side:
    side: str
    distance: int


@mod.action_class
class Actions:
    def move_window_side_to_cursor_position():
        """Move active windows closest side to cursor position"""
        window = ui.active_window()
        rect = window.rect
        x, y = actions.user.mouse_pos()
        side = get_closest_side(rect, x, y)

        if side == "left":
            pos = (x, rect.y, rect.width, rect.height)
        elif side == "right":
            pos = (x - rect.width, rect.y, rect.width, rect.height)
        elif side == "top":
            pos = (rect.x, y, rect.width, rect.height)
        elif side == "bot":
            pos = (rect.x, y - rect.height, rect.width, rect.height)
        elif side == "NOOP":
            return
        else:
            raise Exception(f"Unknown side {side}")

        actions.user.window_set_pos(window, *pos)

    def resize_window_side_to_cursor_position():
        """Resize active windows closest side to cursor position"""
        window = ui.active_window()
        rect = window.rect
        x, y = actions.user.mouse_pos()
        side = get_closest_side(rect, x, y)

        if side == "left":
            pos = (x, rect.y, rect.right - x, rect.height)
        elif side == "right":
            pos = (rect.x, rect.y, x - rect.left, rect.height)
        elif side == "top":
            pos = (rect.x, y, rect.width, rect.bot - y)
        elif side == "bot":
            pos = (rect.x, rect.y, rect.width, y - rect.top)
        elif side == "NOOP":
            return
        else:
            raise Exception(f"Unknown side {side}")

        actions.user.window_set_pos(window, *pos)


def get_closest_side(rect: Rect, x: float, y: float) -> str:
    if not rect.contains(x, y):
        # Between top and bottom
        if y > rect.top and y < rect.bot:
            return "left" if x < rect.left else "right"
        # Between left and right
        if x > rect.left and x < rect.right:
            return "top" if y < rect.bot else "bot"
        # Outside one of the corners.
        return "NOOP"

    sides = []

    sides.append(Side("left", abs(x - rect.left)))
    sides.append(Side("right", abs(x - rect.right)))
    sides.append(Side("top", abs(y - rect.top)))
    sides.append(Side("bot", abs(y - rect.bot)))

    sides.sort(key=lambda side: side.distance)

    return sides[0].side
