from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: linux
tag: terminal
"""

@ctx.action_class('edit')
class EditActions:
    #todo: generic tab commands
    #tag(): tabs
    def page_down():
        actions.key('shift-pagedown')
    def page_up():
        actions.key('shift-pageup')
    def paste():
        actions.key('ctrl-shift-v')
    def copy():
        actions.key('ctrl-shift-c')
    def find(text: str=None):
        actions.key('ctrl-shift-f')
    def word_left():
        actions.key('ctrl-w left')
    def word_right():
        actions.key('ctrl-w right')

@ctx.action_class('app')
class AppActions:
    def tab_open():
        actions.key('ctrl-shift-t')
    def tab_close():
        actions.key('ctrl-shift-w')
    def tab_next():
        actions.key('ctrl-pagedown')
    def tab_previous():
        actions.key('ctrl-pageup')
    def window_open():
        actions.key('ctrl-shift-n')
