from talon import Context, actions, ui, Module, app

mod = Module()

@mod.action_class
class tab_actions:
    def address_copy():
        """Copies the address of the current page"""
