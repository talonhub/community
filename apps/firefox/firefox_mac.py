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

    def window_reopen():
        # Note that as of Firefox 138.0.1, this command does not appear in any Firefox’s menus and only works if there is already an existing Firefox window open.
        actions.key("cmd-shift-n")


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
