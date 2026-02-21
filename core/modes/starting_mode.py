from talon import Module, actions, app, settings

mod = Module()

mod.setting(
    "starting_mode",
    type=str,
    default="command",
    desc="Initial mode for Talon after startup (sleep, command, dictation)",
)


def set_initial_status():
    starting_mode = settings.get("user.starting_mode", "command")
    if starting_mode == "sleep":
        print("Talon ready, entering sleep mode")
        actions.speech.disable()
    elif starting_mode == "dictation":
        print("Talon ready, entering dictation mode")
        actions.user.dictation_mode()
    else:
        pass  # Talon starts in command-mode by default.


app.register("ready", set_initial_status)
