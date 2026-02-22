from talon import Module, actions, app, settings

mod = Module()

mod.setting(
    "starting_mode",
    type=str,
    default="command",
    desc="Mode enabled on Talon launch (sleep, command or dictation)",
)


def enable_starting_mode():
    starting_mode = settings.get("user.starting_mode", "command")
    if starting_mode == "sleep":
        print("Talon ready, in sleep mode")
        actions.speech.disable()
    elif starting_mode == "dictation":
        print("Talon ready, in dictation mode")
        actions.user.dictation_mode()
    else:
        pass  # Talon starts in command mode by default.


app.register("ready", enable_starting_mode)
