from talon import Context, actions, ui, Module, app

mod = Module()

@mod.action_class
class tab_actions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""

    def tab_final():
        """Jumps to the final tab"""

    def tab_close_wrapper():
        """Closes the current tab"""
        actions.app.tab_close()
