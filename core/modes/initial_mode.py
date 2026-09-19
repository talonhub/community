from talon import Module, actions, app, settings

mod = Module()

mod.setting(
    "initial_mode",
    type=str,
    default="command",
    desc="Mode initially enabled on Talon launch (sleep, command or dictation)",
)


def on_ready():
    initial_mode = settings.get("user.initial_mode", "command")
    match initial_mode:
        case "sleep":
            print("Talon ready, in sleep mode")
            actions.speech.disable()
        case "dictation":
            print("Talon ready, in dictation mode")
            actions.user.dictation_mode()
        case "command":
            pass  # already the default; nothing to do
        case _:
            app.notify("Unsupported mode for user.initial_mode: {initial_mode}")


app.register("ready", on_ready)
