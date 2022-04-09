from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: linux
app: microsoft_teams
"""


@ctx.action_class("edit")
class EditActions:
    # zoom in: key(ctrl-=)
    # zoom out: key(ctrl--)
    # reset zoom: key(ctrl-0)
    def zoom_in():
        actions.key("ctrl-=")
    def zoom_out():
        actions.key("ctrl--")

    def zoom_reset():
        actions.key("ctrl-0")
