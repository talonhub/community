from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: windows
os: linux
app: opera
"""


@ctx.action_class("app")
class AppActions:
    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")


@ctx.action_class("browser")
class BrowserActions:
    def bookmarks_bar():
        raise NotImplementedError(
            "Action 'browser.bookmarks_bar' exists but it is not implemented for this Context"
        )

    def bookmarks():
        actions.key("ctrl-shift-b")

    def show_downloads():
        actions.key("ctrl-j")

    def show_extensions():
        actions.key("ctrl-shift-e")

    def focus_page():
        actions.key("f9")
