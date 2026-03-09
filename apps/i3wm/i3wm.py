import subprocess
import time
from typing import Optional, Union

from talon import Context, Module, actions, settings, ui

mod = Module()
ctx = Context()

mod.tag("i3wm", desc="tag for loading i3wm related files")
mod.setting(
    "i3_terminal_key",
    type=str,
    default="super-enter",
    desc="The key combination to launch the preferred terminal",
)
mod.setting(
    "i3_launch_key",
    type=str,
    default="super-d",
    desc="The key combination to start the preferred launcher",
)

ctx.matches = r"""
tag: user.i3wm
"""

mod.list("i3wm_resize_dir", desc="Directions for window resizing in i3wm")


@mod.capture(rule="{user.i3wm_resize_dir}+")
def i3wm_resize_dirs(m) -> str:
    "One or more resize directions separated by a space"
    return str(m)


@ctx.action_class("app")
class AppActions:
    def window_close():
        subprocess.check_call(("i3-msg", "kill"))


def i3msg_nocheck(arguments: str):  # type: ignore
    """Call i3-msg on space-separated arguments"""
    subprocess.run(
        ["i3-msg", "--quiet"] + arguments.split(" "),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


# For i3wm we cannot rely on the focusing functions from the UI toolkit, because
# i3wm treats this like the application is trying to acquire focus on its own.
# The default reaction of i3wm to such requests from windows on another
# workspace is to downgrade this to setting the "urgent" flag. Is violates the
# implicit contract of commands like those for the draft editor, which rely on
# the focus commands successfully changing the focus.
def i3wm_focus_window_by_id(id: int):
    actions.user.i3msg(f"[id={id}] focus")


_switcher_focus_windows_to_skip: set[int] = set()


@ctx.action_class("user")
class UserActions:
    def switcher_focus_window(window: ui.Window):  # type: ignore
        i3wm_focus_window_by_id(window.id)

    def switcher_focus(name: str):  # type: ignore
        global _switcher_focus_windows_to_skip
        app = actions.user.get_running_app(name)

        # If app is inactive, focus most recently active window
        if app != ui.active_app():
            i3wm_focus_window_by_id(app.active_window.id)

        # Otherwise, cycle through available windows
        app_window_ids: list[int] = [
            window.id for window in app.windows() if not window.hidden
        ]
        assert len(app_window_ids) > 0

        _switcher_focus_windows_to_skip.add(ui.active_window().id)
        targets = [
            id for id in app_window_ids if id not in _switcher_focus_windows_to_skip
        ]
        if len(targets) > 0:
            # focus new window if one is available
            i3wm_focus_window_by_id(targets[0])
        else:
            # otherwise, focus window that is furthest down the stack
            _switcher_focus_windows_to_skip = set()
            i3wm_focus_window_by_id(app_window_ids[-1])

    def switcher_focus_app(app: ui.App):  # type: ignore
        i3wm_focus_window_by_id(app.active_window.id)

        t1 = time.perf_counter()
        while ui.active_app() != app:
            if time.perf_counter() - t1 > 1:
                raise RuntimeError(f"Can't focus app: {app.name}")
            actions.sleep(0.1)

    # the default implementation considers desktops consecutively numbered
    # this would be highly confusing given the numbering of i3wm workspaces
    def desktop(number: int):  # type: ignore
        actions.user.i3msg(f"workspace number {number}")

    def desktop_next():
        actions.user.i3msg(f"workspace next")

    def desktop_last():
        actions.user.i3msg(f"workspace prev")


@mod.action_class
class Actions:
    def i3msg(arguments: str):  # type: ignore
        """Call i3-msg on space-separated arguments"""
        subprocess.check_call(["i3-msg", "--quiet"] + arguments.split(" "))

    def i3wm_resize_window(op: str, amount: int, directions: str):  # type: ignore
        """Resize window by specified amount and direction (in steps of 10 pixels)"""
        for dir in directions.split(" "):
            i3msg_nocheck(f"resize {op} {dir} {10 * amount}")

    def i3wm_layout(layout: Optional[str] = None):  # type: ignore
        """Change to specified layout. Toggle split if unspecified."""
        if layout is None:
            actions.user.i3msg("layout toggle split")
        else:
            actions.user.i3msg(f"layout {layout}")

    # TODO The remaining functions hard code default keybindings for actions
    # that are commonly customized in the config file. Make this configuration
    # more visible.

    def i3wm_launch():
        """Trigger the i3 launcher: ex rofi"""
        key = settings.get("user.i3_launch_key")
        actions.key(key)

    def i3wm_shell():
        """Launch a shell"""
        key = settings.get("user.i3_terminal_key")
        actions.key(key)
