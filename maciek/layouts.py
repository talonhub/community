from typing import List
from ..code.window_snap import (
    RelativeScreenPos,
    get_app_window,
    get_screen_number,
    move_to_screen,
    sorted_screens,
)
from talon import Context, Module, actions, app, ui


Layout = List[tuple[str, int, RelativeScreenPos]]


layout1 = [
    ("code", 2, RelativeScreenPos(0, 0, 1, 1)),
    ("chrome", 3, RelativeScreenPos(0, 0, 1, 1)),
    ("slack", 1, RelativeScreenPos(0, 0, 1, 1)),
    ("obsidian", 1, RelativeScreenPos(0, 0, 1, 1)),
    ("kitty", 1, RelativeScreenPos(0, 0, 1, 1)),
]
layouts = {"one": layout1}


mod = Module()
ctx = Context()
# mod.list("layouts", desc="list of layout")
# ctx.lists["self.layouts"] = layouts.keys()


@mod.capture(rule="one")
def layout(m) -> Layout:
    """this is mandatory doc string"""
    # print("fsdafadsfadfjdsa", type(m[0]))
    # print(layouts["one"])
    return layouts[str(m)]


def move_window_to_screen_rect(window, screen_number, rect):
    move_to_screen(window, screen_number)
    window.rect = rect


@mod.action_class
class Actions:
    def activate_layout(layout: Layout):
        """This description is mandatory"""
        # print("activate layout!!")
        # print(sorted_screens())
        for app_name, screen_idx, relative_screen_pos in layout:
            # print(f"will be moving {app_name} to {screen_idx} screen")
            try:
                actions.user.move_app_to_screen(app_name, screen_idx)
                actions.user.snap_app(app_name, relative_screen_pos)
            except Exception as e:
                continue

    def exchange_windows(app_name: str):
        """This description is mandatory"""
        active_window = ui.active_window()
        other_window = get_app_window(app_name)
        # print(f"active_window =  {active_window}")
        # print(f"other_window =  {other_window}")
        screen_number_1 = get_screen_number(active_window.screen)
        rect_1 = active_window.rect
        # print(screen_number_1, rect_1)

        screen_number_2 = get_screen_number(other_window.screen)
        rect_2 = other_window.rect
        # print(screen_number_2, rect_2)
        move_window_to_screen_rect(active_window, screen_number_2, rect_2)
        move_window_to_screen_rect(other_window, screen_number_1, rect_1)
