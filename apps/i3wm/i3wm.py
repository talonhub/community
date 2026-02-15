import subprocess
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

@ctx.action_class("user")
class UserActions:
    def switcher_focus_window(window: ui.Window):  # type: ignore
        i3wm_focus_window_by_id(window.id)

    def switcher_focus(name: str):  # type: ignore
        app = actions.user.get_running_app(name)
        actions.user.switcher_focus_app(app)

    def switcher_focus_app(app: ui.App):  # type: ignore
        # Obtain window ids for all windows of the application
        # (sorting is necessary, because the order differs between calls)
        app_window_ids: list[int] = sorted([window.id for window in app.windows() ])
        assert(len(app_window_ids) > 0)

        if app == ui.active_app():
            # Focus next window of already active app
            current_idx = app_window_ids.index(app.active_window.id)
            next_idx = (current_idx + 1) % len(app_window_ids)
            i3wm_focus_window_by_id(app_window_ids[next_idx])
        else:
            # Focus first window of previously inactive app
            i3wm_focus_window_by_id(app_window_ids[0])

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
