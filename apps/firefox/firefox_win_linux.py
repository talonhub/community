from talon import Context, actions, app

ctx = Context()

ctx.matches = r"""
os: windows
os: linux
tag: browser
app: firefox
"""


@ctx.action_class("user")
class UserActions:
    def firefox_bookmarks_sidebar():
        actions.key("ctrl-b")

    def firefox_history_sidebar():
        actions.key("ctrl-h")


@ctx.action_class("browser")
class BrowserActions:
    def focus_address():
        # Only using "ctrl-l" might fail and clear the console if the user
        # is focused in the devtools
        actions.key("f6")
        actions.sleep("100ms")
        actions.key("ctrl-l")

    def open_private_window():
        actions.key("ctrl-shift-p")

    def show_downloads():
        if app.platform == "linux":
            actions.key("ctrl-shift-y")
        else:
            actions.key("ctrl-j")

    def show_extensions():
        actions.key("ctrl-shift-a")

    def show_history():
        actions.key("ctrl-shift-h")
