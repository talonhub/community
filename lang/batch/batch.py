from talon import Context, actions

ctx = Context()
ctx.matches = r"""
tag: user.batch
"""


@ctx.action_class("user")
class UserActions:
    # tag(): user.code_generic
    def code_comment_line_prefix():
        actions.auto_insert("REM ")
