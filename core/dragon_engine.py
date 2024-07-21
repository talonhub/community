from talon import Module, speech_system

mod = Module()


@mod.action_class
class Actions:
    def dragon_engine_sleep():
        """Sleep the dragon engine"""
        speech_system.engine_mimic("go to sleep"),

    def dragon_engine_wake():
        """Wake the dragon engine"""
        speech_system.engine_mimic("wake up"),

    def dragon_engine_command_mode():
        """Switch dragon to command mode. Requires Pro."""
        speech_system.engine_mimic("switch to command mode")

    def dragon_engine_normal_mode():
        """Switch dragon to normal mode. Requires Pro."""
        speech_system.engine_mimic("start normal mode")
