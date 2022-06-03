from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: mac
tag: user.fish
"""

@ctx.action_class('edit')
class EditActions:
    def delete_word():
        actions.edit.word_right()
        actions.key('ctrl-w')
