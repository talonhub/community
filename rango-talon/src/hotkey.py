from talon import Module, actions

mod = Module()

_HOTKEY = "ctrl-shift-insert"


@mod.action_class
class Actions:
    def rango_type_hotkey():
        """Presses the rango hotkey to read the command from the clipboard"""
        actions.key(_HOTKEY)
