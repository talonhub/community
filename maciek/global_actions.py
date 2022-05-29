from talon import Context, actions, ui, Module, app
import time

mod = Module()


@mod.action_class
class Actions:
    def maciek_speech_toggle():
        """
        Vanilla actions.speech.toggle() does not handle well situations
        where we are in the polish dictation mode. This fixes that.
        """
        if actions.speech.enabled():
            actions.user.command_mode()
            actions.speech.disable()
        else:
            actions.speech.enable()
