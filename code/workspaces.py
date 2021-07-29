from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def workspace_next():
        """Move to next workspace"""

    def workspace_last():
        """Move to previous workspace"""

    def workspace_show():
        """Show / manage workspaces"""
