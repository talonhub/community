import subprocess
from typing import Optional, Union

from talon import Context, Module, actions, settings, ui

mod = Module()
ctx = Context()

mod.tag("i3wm", desc="tag for loading i3wm related files")
mod.setting(
    "i3_config_path",
    type=str,
    default="~/.i3/config",
    desc="Where to find the configuration path",
)
mod.setting(
    "i3_mod_key",
    type=str,
    default="super",
    desc="The default key to use for i3wm commands",
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
        key = settings.get("user.i3_mod_key")
        actions.key(f"{key}-d")

    def i3wm_shell():
        """Launch a shell"""
        key = settings.get("user.i3_mod_key")
        actions.key(f"{key}-enter")

    def i3wm_lock():
        """Trigger the lock screen"""
        key = settings.get("user.i3_mod_key")
        actions.key(f"{key}-shift-x")
