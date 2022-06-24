from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: linux
app: Guake
"""
ctx.tags = ["user.git", "user.kubectl", "user.tabs", "terminal"]


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_close():
        actions.key("ctrl-shift-w")

    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")
