from talon import Module, app, actions, settings

mod = Module()

mod.setting(
    "starting_mode",
    type=str,
    default="command",
    desc="Initial mode for Talon after startup (sleep, command, dictation)"
)

def set_initial_status():
    starting_mode = settings.get("user.starting_mode", "command")
    print(f"setting initial mode to {starting_mode}")
    if starting_mode == "sleep":
        actions.speech.disable()
    elif starting_mode == "dictation":
        actions.mode.disable("sleep")
        actions.mode.disable("command")
        actions.mode.enable("dictation")
    else:
        pass # Talon starts in command-mode by default.


app.register("ready", set_initial_status)
