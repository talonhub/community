from talon import Context, Module, app, actions

mod = Module()

modes = {
    "admin": "enable extra administration commands terminal (docker, etc)",
    "debug": "a way to force debugger commands to be loaded",
    "gdb": "a way to force gdb commands to be loaded",
    "ida": "a way to force ida commands to be loaded",
    "presentation": "a more strict form of sleep where only a more strict wake up command works",
    "windbg": "a way to force windbg commands to be loaded",
}

for key, value in modes.items():
    mod.mode(key, value)


@mod.action_class
class Actions:
    def talon_mode():
        """For windows and Mac, enables Talon commands and enables command mode or equivalent."""

        actions.speech.enable()
        if app.platform == "mac":
            actions.user.engine_sleep()
        elif app.platform == "windows":
            actions.user.engine_wake()

            # note: this may not do anything for all versions of Dragon. Requires Pro.
            actions.user.engine_mimic("switch to command mode")

    def dragon_mode():
        """For windows and Mac, disables Talon commands and exits command mode or equivalent."""
        actions.speech.disable()
        if app.platform == "mac":
            actions.user.engine_wake()
        elif app.platform == "windows":
            actions.user.engine_wake()
            # note: this may not do anything for all versions of Dragon. Requires Pro.
            actions.user.engine_mimic("start normal mode")
