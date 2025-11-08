import subprocess
from typing import Optional, Union

from talon import Context, Module, actions, settings

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

ctx.matches = """
tag: user.i3wm
"""


@ctx.action_class("app")
class AppActions:
    def window_close():
        subprocess.check_call(("i3-msg", "kill"))


@mod.action_class
class Actions:
    def i3msg(arguments: str): # type: ignore
        """Call i3-msg on space-separated arguments"""
        subprocess.check_call(["i3-msg", "--quiet"]+arguments.split(" "))

    def i3wm_grow_window(amount: int): # type: ignore
        """Grow window by specified amount (in pixels)"""
        actions.user.i3msg(f"resize grow width {amount}; resize grow height {amount}")
        actions.user.i3msg(f"move left {int(amount / 2)}; move up {int(amount / 2)}")

    def i3wm_shrink_window(amount: int): # type: ignore
        """Shrink window by specified amount (in pixels)"""
        actions.user.i3msg(f"resize shrink width {amount}; resize shrink height {amount}")
        actions.user.i3msg(f"move right {int(amount / 2)}; move down {int(amount / 2)}")

    def i3wm_layout(layout: Optional[str] = None): # type: ignore
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
