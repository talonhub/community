from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def speech_toggle():
        """Toggle speech on and off"""
        if actions.speech.enabled():
            actions.speech.disable()
        else:
            actions.speech.enable()
