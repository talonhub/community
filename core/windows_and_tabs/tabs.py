from talon import Module, actions, app

mod = Module()


@mod.action_class
class tab_actions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""

    def tab_final():
        """Jumps to the final tab"""

    def tab_close_wrapper():
        """Closes the current tab.
        Exists so that apps can implement their own delay before running tab_close() to handle repetitions better.
        """
        actions.app.tab_close()

    def tab_duplicate():
        """Duplicates the current tab."""

    def tab_close_others():
        """Closes all other tabs"""
        
    def tab_close_all():
        """Closes all tabs"""

    def tab_close_right():
        """Closes all tabs to the right"""

    def tab_close_left():
        """ closes taps to the left"""

    def tab_search(string: str): 
        """ Executes tab search command"""