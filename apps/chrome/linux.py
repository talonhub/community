from talon import Context, actions

ctx = Context()
ctx.matches = """
os: linux
app: chrome
"""
ctx.tags = ["browser", "user.tabs"]


@ctx.action_class("browser")
class BrowserActions:
    def bookmark():
        actions.key("ctrl-d")

    def bookmarks():
        actions.key("ctrl-shift-o")

    def bookmarks_bar():
        actions.key("ctrl-shift-b")

    def focus_address():
        actions.key("ctrl-l")

    def focus_search():
        actions.browser.focus_address()

    def go_blank():
        actions.key("ctrl-n")

    def go_back():
        actions.key("alt-left")

    def go_forward():
        actions.key("alt-right")

    def go_home():
        actions.key("alt-home")

    def open_private_window():
        actions.key("ctrl-shift-n")

    def reload():
        actions.key("ctrl-r")

    def reload_hard():
        actions.key("ctrl-shift-r")

    def show_downloads():
        actions.key("ctrl-j")

    def show_history():
        actions.key("ctrl-h")

    def submit_form():
        actions.key("enter")

    def toggle_dev_tools():
        actions.key("ctrl-shift-i")
