from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: mac
app: finder
"""

@ctx.action_class('user')
class UserActions:
    def file_manager_open_parent():
        actions.key('cmd-up')
    def file_manager_go_forward():
        actions.key('cmd-]')
    def file_manager_go_back():
        actions.key('cmd-[')
