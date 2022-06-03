from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: linux
tag: terminal
"""

@ctx.action_class('edit')
class EditActions:
    def word_left():
        actions.key('ctrl-w left')
    def word_right():
        actions.key('ctrl-w right')

@ctx.action_class('app')
class AppActions:
    def window_open():
        actions.key('ctrl-shift-n')
