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
    def i3wm_mode(name: str):
        """Switch i3 mode"""
        subprocess.check_call(("i3-msg", "mode", name))

    def i3wm_reload():
        """Reload the i3 config"""
        subprocess.check_call(("i3-msg", "reload"))

    def i3wm_restart():
        """Restart the window manager"""
        subprocess.check_call(("i3-msg", "restart"))

    def i3wm_layout(layout: Optional[str] = None):
        """Change to specified layout. Toggle split if unspecified."""
        if layout is None:
            subprocess.check_call(("i3-msg", "layout", "toggle", "split"))
        else:
            subprocess.check_call(("i3-msg", "layout", layout))

    def i3wm_fullscreen():
        """Fullscreen the current container"""
        subprocess.check_call(("i3-msg", "fullscreen"))

    def i3wm_split(direction: str):
        """Split the focused container"""
        subprocess.check_call(("i3-msg", "split", direction))

    def i3wm_float():
        """Toggle whether the focused container should float."""
        subprocess.check_call(("i3-msg", "floating", "toggle"))

    def i3wm_launch():
        """Trigger the i3 launcher: ex rofi"""
        key = settings.get("user.i3_mod_key")
        actions.key(f"{key}-d")

    def i3wm_shell():
        """Launch a shell"""
        key = settings.get("user.i3_mod_key")
        actions.key(f"{key}-enter")

    def i3wm_focus(what: str):
        """Move focus"""
        subprocess.check_call(("i3-msg", "focus", what))

    def i3wm_switch_to_workspace(which: Union[str, int]):
        """Focus the specified workspace"""
        if isinstance(which, int):
            subprocess.check_call(("i3-msg", "workspace", "number", str(which)))
        else:
            subprocess.check_call(("i3-msg", "workspace", which))

    def i3wm_show_scratchpad():
        """Focus/cycle/hide the scratchpad"""
        subprocess.check_call(("i3-msg", "scratchpad", "show"))

    def i3wm_move(to: str):
        """Move the focused container"""
        subprocess.check_call(("i3-msg", "move", to))

    def i3wm_move_to_workspace(which: Union[str, int]):
        """Move the focused container to the specified workspace"""
        if isinstance(which, int):
            subprocess.check_call(
                ("i3-msg", "move", "container", "to", "workspace", "number", str(which))
            )
        else:
            subprocess.check_call(
                ("i3-msg", "move", "container", "to", "workspace", which)
            )

    def i3wm_move_to_output(which: str):
        """Move the focused container to the specified output."""
        subprocess.check_call(("i3-msg", "move", "container", "to", "output", which))

    def i3wm_move_position(where: str):
        """Move the focused container to the specified position."""
        subprocess.check_call(("i3-msg", "move", "position", where))

    def i3wm_lock():
        """Trigger the lock screen"""
        key = settings.get("user.i3_mod_key")
        actions.key(f"{key}-shift-x")
