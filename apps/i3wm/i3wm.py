from talon import Module, actions, settings

mod = Module()

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


@mod.action_class
class Actions:
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
