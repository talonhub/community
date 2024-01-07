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
        if settings.get("user.log_level") == "debug":
            print(f"DEBUG: {message}")

    def info(message: str):
        """Log info message"""
        if settings.get("user.log_level") in ["debug", "info"]:
            print(f"INFO: {message}")
