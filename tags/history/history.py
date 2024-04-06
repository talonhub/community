from talon import Module, Context, actions

mod = Module()
mod.tag("history", desc="enables the history commands")

@mod.action_class
class Actions:
    def history_go_back():
        """Action to go back a page in the history"""
    
    def history_go_forward():
        """Action to go forward a page in the history"""