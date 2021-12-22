from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: mac
"""

@ctx.action_class('app')
class AppActions:
    def preferences():
        actions.key('cmd-,')
    def tab_close():
        actions.key('cmd-w')
        #action(app.tab_detach):
        #  Move the current tab to a new window
    def tab_next():
        actions.key('cmd-shift-]')
    def tab_open():
        actions.key('cmd-t')
    def tab_previous():
        actions.key('cmd-shift-[')
    def tab_reopen():
        actions.key('cmd-shift-t')
    def window_close():
        actions.key('cmd-w')
    def window_hide():
        actions.key('cmd-m')
    def window_hide_others():
        actions.key('cmd-alt-h')
    def window_next():
        actions.key('cmd-`')
    def window_open():
        actions.key('cmd-n')
    def window_previous():
        actions.key('cmd-shift-`')
