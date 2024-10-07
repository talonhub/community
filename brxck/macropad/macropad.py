from talon import Module, Context, actions

mod = Module()

@mod.action_class
class MacroPadActions:
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
        """Toggle between command and dictation mode"""
        pass

ctx = Context()
ctx.matches = "mode: command"

@ctx.action_class("user")
class MacroPadActionsCommand:
    def mode_toggle():
        actions.app.notify("Dictation mode")
        actions.mode.enable("dictation")
        actions.mode.disable("command")
        
ctx = Context()
ctx.matches = "mode: dictation"

@ctx.action_class("user")
class MacroPadActionsDictation:
    def mode_toggle():
        actions.app.notify("Command mode")
        actions.mode.enable("command")
        actions.mode.disable("dictation")
        