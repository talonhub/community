from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: linux
app: Firefox
app: firefox
"""


@ctx.action_class("app")
class AppActions:
    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")


@ctx.action_class("browser")
class BrowserActions:
    def bookmark():
        actions.key("ctrl-d")

    def bookmark_tabs():
        actions.key("ctrl-shift-d")

    def bookmarks():
        actions.key("ctrl-shift-o")

    def bookmarks_bar():
        actions.key("ctrl-b")

    def focus_address():
        actions.key("ctrl-l")
        # action(browser.focus_page):

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
        actions.key("ctrl-shift-r")
        # action(browser.reload_hardest):

    def show_clear_cache():
        actions.key("ctrl-shift-del")

    def show_downloads():
        actions.key("ctrl-shift-y")

    def show_extensions():
        actions.key("ctrl-shift-a")

    def show_history():
        actions.key("ctrl-h")

    def toggle_dev_tools():
        actions.key("ctrl-shift-i")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"alt-{number}")

    def tab_final():
        actions.key("alt-9")
