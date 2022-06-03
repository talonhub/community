from talon import Context, actions
ctx = Context()
ctx.matches = r"""
app: apple_terminal
"""

@ctx.action_class('user')
class UserActions:
    def file_manager_open_parent():
        actions.insert('cd ..')
        actions.key('enter')

@ctx.action_class('app')
class AppActions:
    def tab_open():
        actions.key('cmd-t')
    def tab_close():
        actions.key('cmd-w')
    def tab_next():
        actions.key('ctrl-tab')
    def tab_previous():
        actions.key('ctrl-shift-tab')
    def window_open():
        actions.key('cmd-n')

@ctx.action_class('edit')
class EditActions:
    def page_down():
        actions.key('command-pagedown')
    def page_up():
        actions.key('command-pageup')
