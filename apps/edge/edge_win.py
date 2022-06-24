from talon import Context, actions

ctx = Context()

ctx.matches = r"""
os: windows
app: microsoft_edge
"""
ctx.tags = ["browser", "user.tabs"]


@ctx.action_class("browser")
class BrowserActions:
    # action(browser.address):

    def bookmark():
        actions.key("ctrl-d")

    def bookmark_tabs():
        actions.key("ctrl-shift-d")

    def bookmarks():
        actions.key("ctrl-shift-o")

    def bookmarks_bar():
        actions.key("ctrl-shift-b")

    def focus_address():
        actions.key("ctrl-l")
        # action(browser.focus_page):

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
        actions.key("ctrl-shift-p")

    def reload():
        actions.key("ctrl-r")

    def reload_hard():
        actions.key("shift-f5")
        # action(browser.reload_hardest):

    def show_clear_cache():
        actions.key("ctrl-shift-delete")

    def show_downloads():
        actions.key("ctrl-j")
        # action(browser.show_extensions)

    def show_history():
        actions.key("ctrl-h")

    def submit_form():
        actions.key("enter")
        # action(browser.title)

    def toggle_dev_tools():
        actions.key("ctrl-shift-i")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"ctrl-{number}")

    def tab_final():
        actions.key("ctrl-9")
