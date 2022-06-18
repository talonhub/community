from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app: notes
"""


@ctx.action_class("edit")
class EditActions:
    def zoom_in():
        actions.key("shift-cmd->")

    def zoom_out():
        actions.key("shift-cmd-<")

    def zoom_reset():
        actions.key("shift-cmd-0")

    def indent_less():
        actions.key("cmd-[")
