from talon import Module, speech_system

mod = Module()


@mod.action_class
class Actions:
    def engine_sleep():
        """Sleep the engine"""
        speech_system.engine_mimic("go to sleep"),

    def engine_wake():
        """Wake the engine"""
        speech_system.engine_mimic("wake up"),

    def engine_mimic(cmd: str):
        """Sends phrase to engine"""
        speech_system.engine_mimic(cmd)
