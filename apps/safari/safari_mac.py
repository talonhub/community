from talon import Context, Module, actions, ui
from talon.mac import applescript

ctx = Context()
mod = Module()
apps = mod.apps
mod.apps.safari = """
os: mac
and app.bundle: com.apple.Safari
"""

ctx.matches = r"""
app: safari
"""
ctx.tags = ["browser", "user.tabs"]


def safari_app():
    return ui.apps(bundle="com.apple.Safari")[0]


@ctx.action_class("browser")
class BrowserActions:
    def address() -> str:
        try:
            window = safari_app().windows()[0]
        except IndexError:
            return ""
        try:
            toolbar = window.children.find_one(AXRole="AXToolbar", max_depth=0)
            address_field = toolbar.children.find_one(
                AXRole="AXTextField",
                AXIdentifier="WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD",
            )
            address = address_field.AXValue
        except (ui.UIErr, AttributeError):
            address = applescript.run(
                """
                tell application id "com.apple.Safari"
                    with timeout of 0.1 seconds
                        if not (exists (window 1)) then return ""
                        return window 1's current tab's URL
                    end timeout
                end tell
            """
            )
        return address

    def bookmark():
        actions.key("cmd-d")

    def bookmark_tabs():
        actions.key("cmd-shift-d")

    def bookmarks():
        actions.key("ctrl-cmd-1")
        # action(browser.bookmarks_bar):
        # 	key(ctrl-shift-b)

    def focus_address():
        actions.key("cmd-l")
        # action(browser.focus_page):

    def focus_search():
        actions.browser.focus_address()

    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("enter")

    def go_blank():
        actions.key("cmd-n")

    def go_back():
        actions.key("cmd-[")

    def go_forward():
        actions.key("cmd-]")

    def go_home():
        actions.key("cmd-shift-h")

    def open_private_window():
        actions.key("cmd-shift-n")

    def reload():
        actions.key("cmd-r")

    def reload_hard():
        actions.key("cmd-shift-r")
        # action(browser.reload_hardest):
        # action(browser.show_clear_cache):
        # 	key(cmd-shift-delete)

    def show_downloads():
        actions.key("cmd-alt-l")

    # def show_extensions():
    #     actions.key('ctrl-shift-a')
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
            actions.key(f"cmd-{number}")

    def tab_final():
        actions.key("cmd-9")
