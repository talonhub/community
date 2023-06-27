from talon import Context, actions

ctx = Context()

ctx.matches = r"""
os: mac
tag: browser
app: firefox
"""


@ctx.action_class("user")
class UserActions:
    def firefox_bookmarks_sidebar():
        actions.key("cmd-b")

    def firefox_history_sidebar():
        actions.key("cmd-shift-h")


@ctx.action_class("browser")
class BrowserActions:
    def bookmarks():
        actions.key("cmd-shift-o")

    def open_private_window():
        actions.key("cmd-shift-p")

    def show_downloads():
        actions.key("cmd-j")

    def show_extensions():
        actions.key("cmd-shift-a")
