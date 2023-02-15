from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app: opera
"""


@ctx.action_class("browser")
class BrowserActions:
    def show_downloads():
        actions.key("cmd-j")

    def show_extensions():
        actions.key("cmd-shift-e")

    def show_history():
        actions.key("cmd-shift-h")

    def focus_page():
        actions.key("cmd-alt-l")
