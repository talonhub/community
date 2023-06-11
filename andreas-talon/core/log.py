from talon import Module

mod = Module()

setting_level = mod.setting(
    "log_level",
    type=str,
    default="info",
)


@mod.action_class
class Actions:
    def debug(message: str):
        """Log debug message"""
        if setting_level.get() == "debug":
            print(f"DEBUG: {message}")

    def info(message: str):
        """Log info message"""
        if setting_level.get() in ["debug", "info"]:
            print(f"INFO: {message}")
