from talon import Context, actions, app, mac, ui
from talon.mac import applescript

ctx = Context()
ctx.matches = r"""
os: mac
tag: browser
"""


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"cmd-{number}")

    def tab_final():
        actions.key("cmd-9")


@ctx.action_class("browser")
class BrowserActions:
    def address():
        try:
            mac_app = ui.apps(bundle=actions.app.bundle())[0]
            window = mac_app.windows()[0]
        except IndexError:
            return ""
        try:
            web_area = window.element.children.find_one(AXRole="AXWebArea")
            address = web_area.AXURL
        except (ui.UIErr, AttributeError):
            try:
                address = applescript.run(
                    """
                    tell application id "{bundle}"
                        if not (exists (window 1)) then return ""
                        return the URL of the active tab of the front window
                    end tell""".format(
                        bundle=actions.app.bundle()
                    )
                )
            except mac.applescript.ApplescriptErr:
                return actions.next()
        return address

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

    def go_blank():
        actions.key("cmd-n")

    def go_home():
        actions.key("cmd-shift-h")

    def go_back():
        actions.key("cmd-[")

    def go_forward():
        actions.key("cmd-]")

    def open_private_window():
        actions.key("cmd-shift-n")

    def reload():
        actions.key("cmd-r")

    def reload_hard():
        actions.key("cmd-shift-r")

    def show_downloads():
        actions.key("cmd-shift-j")

    def show_clear_cache():
        actions.key("cmd-shift-backspace")

    def show_history():
        actions.key("cmd-y")

    def toggle_dev_tools():
        actions.key("cmd-alt-i")
