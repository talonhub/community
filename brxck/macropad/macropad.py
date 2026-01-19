from talon import Module, Context, actions, scope

mod = Module()

_wispr_speech_was_enabled = False

@mod.action_class
class MacroPadActions:
    def wispr_toggle_down():
        """Disable speech for wispr if it was enabled, tracking state for re-enable on up"""
        global _wispr_speech_was_enabled
        _wispr_speech_was_enabled = actions.speech.enabled()
        if _wispr_speech_was_enabled:
            actions.speech.disable()
        actions.key("ctrl-alt-b:down")

    def wispr_toggle_up():
        """Re-enable speech after wispr if it was enabled before"""
        global _wispr_speech_was_enabled
        actions.key("ctrl-alt-b:up")
        if _wispr_speech_was_enabled:
            actions.speech.enable()

    def speech_toggle_down():
        """Toggle speech on and off"""
        if actions.speech.enabled():
            actions.speech.disable()
        else:
            actions.user.delayed_speech_on()
                
    def speech_toggle_up():
        """Toggle speech on and off"""
        if actions.user.is_delayed_enabled():
            actions.user.delayed_speech_off()
        else:
            actions.speech.enable()
            
    def mode_toggle():
        """Toggle between command, dictation, and mixed mode"""
        mode = scope.get("mode")
        if {'command', 'dictation'}.issubset(mode):
            actions.app.notify("Command mode")
            actions.mode.enable("command")
            actions.mode.disable("dictation")
        elif 'command' in mode:
            actions.app.notify("Dictation mode")
            actions.mode.enable("dictation")
            actions.mode.disable("command")
        elif 'dictation' in mode:
            actions.app.notify("Mixed mode")
            actions.mode.enable("command")
            actions.mode.enable("dictation")
