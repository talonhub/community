from talon import Context, Module, actions
ctx = Context()
ctx.matches = r"""
os: windows
"""

@ctx.action_class('user')
class UserActions:
    def workspace_next():
        """Move to next workspace"""
        actions.key('ctrl-super-right')

    def workspace_last():
        """Move to previous workspace"""
        actions.key('ctrl-super-left')

    def workspace_show():
        """Show / manage workspaces"""
        actions.key('super-tab')
