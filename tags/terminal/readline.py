from talon import Context, actions

ctx = Context()
ctx.matches = r"""
tag: user.readline
"""


@ctx.action_class("edit")
class Actions:
    def delete_line():
        actions.key("ctrl-e")
        actions.key("ctrl-u")
