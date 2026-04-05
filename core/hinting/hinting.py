from talon import (
    Context,
    Module,
    actions,
    app,
    canvas,
    cron,
    ctrl,
    imgui,
    resource,
    settings,
    ui,
)
from talon.ui import Rect

from ..operating_system.windows.accessibility import (
    find_all_clickable_rects,
    find_all_clickables_in_list_parallel,
    get_window_class,
)

mod = Module()
mod.tag("hinting_active", desc="Indicates hints are active")
mod.setting(
    "hinting_auto_hint_menus",
    type=bool,
    default=False,
    desc="Enables experimental auto-hinting of menus",
)
mod.setting(
    "hinting_filter_overlapping_item",
    type=bool,
    default=True,
    desc="Enables filtering of overlapping rects",
)
mod.setting(
    "hinting_filter_using_actions",
    type=bool,
    default=False,
    desc="Enables filtering of elements without AXPress, AXShowMenu or similar actions",
)

mod.setting(
    "hinting_filter_using_element_at",
    type=bool,
    default=False,
    desc="Enables filtering of elements without AXPress, AXShowMenu or similar actions",
)

mod.setting(
    "hinting_iou_threshold",
    type=float,
    default=0.15,
    desc="Sets min threshold for eliminating overlapping elements",
)


ctx = Context()


@mod.capture(rule="<user.letter> (twice | second)")
def hinting_double(m) -> str:
    return m.letter + m.letter


@mod.capture(
    rule="<user.letter> | <user.letter> <user.letter> | <user.hinting_double> "
)
def hinting(m) -> str:
    return "".join(m)


@ctx.action_class("main")
class MainActions:
    def mouse_click(button: int = 0):
        actions.user.hinting_close(True)
        actions.next(button)

    def mouse_scroll(y: float = 0, x: float = 0, by_lines: bool = False):
        actions.user.hinting_close(True)
        actions.next(y, x, by_lines)


@mod.action_class
class Actions:
    def hinting_close(clear_cache: True):
        """Closes hinting canvas if open"""
        return False

    def hinting_toggle():
        """Toggles hints"""
        pass

    def hinting_select(mouse_button: int, label: str, click_count: int):
        """Click the hint based on the index"""
        pass
