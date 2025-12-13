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


@ctx.action_class("user")
class UserActions:
    def switcher_focus(name: str):  # type: ignore
        app = actions.user.get_running_app(name)

        if app == ui.active_app():
            # Focus next window on same app
            actions.app.window_next()
        else:
            # Focus first window of app
            app.focus()
        # Make sure we really focus the window, even if
        # focus_on_window_activation is set to "smart" or "urgent"
        actions.user.i3msg('[urgent="latest"] focus')

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
