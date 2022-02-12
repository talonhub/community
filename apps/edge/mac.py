from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app: microsoft_edge
"""
ctx.tags = ["browser", "user.tabs"]


@ctx.action_class("browser")
class BrowserActions:
    # action(browser.address):

    def bookmark():
        actions.key("cmd-d")

    def bookmark_tabs():
        actions.key("cmd-shift-d")

    def bookmarks():
        actions.key("cmd-alt-b")

    def bookmarks_bar():
        actions.key("cmd-shift-b")

    def focus_address():
        actions.key("cmd-l")
        # action(browser.focus_page):

    def focus_search():
        actions.browser.focus_address()

    def go_blank():
        actions.key("cmd-n")

    def go_back():
        actions.key("cmd-left")

    def go_forward():
        actions.key("cmd-right")

    def go_home():
        actions.key("cmd-shift-h")

    def open_private_window():
        actions.key("cmd-shift-n")

    def reload():
        actions.key("cmd-r")

    def reload_hard():
        actions.key("shift-cmd-r")
        # action(browser.reload_hardest):

    def show_clear_cache():
        actions.key("cmd-shift-delete")

    def show_downloads():
        actions.key("cmd-shift-j")
        # action(browser.show_extensions)

    def show_history():
        actions.key("cmd-y")

    def submit_form():
        actions.key("enter")
        # action(browser.title)

    def toggle_dev_tools():
        actions.key("cmd-alt-i")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key("cmd-{}".format(number))

    def tab_final():
        actions.key("cmd-9")
