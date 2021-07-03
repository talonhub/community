from talon import Context, actions

ctx = Context()
ctx.matches = r"""
mode: user.batch
mode: user.auto_lang
and code.language: batch
"""


@ctx.action_class("user")
class UserActions:
    # tag(): user.code_generic
    def code_comment():
        actions.auto_insert("REM ")

