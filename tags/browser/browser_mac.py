from talon import Context, actions, app, mac, ui

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
            # for Firefox and Chromium-based browsers (if accessibility available)
            addresses = [
                web_area.AXURL for web_area in window.children.find(AXRole="AXWebArea")
            ]
            match len(addresses):
                case 0:
                    pass
                case 1:
                    return addresses[0]
                case _:
                    addresses = [
                        a
                        for a in addresses
                        if not (
                            a.startswith("devtools:")
                            or a.startswith("about:devtools")
                            or a.startswith("chrome://devtools/")
                        )
                    ]
                    if len(addresses) == 1:
                        return addresses[0]
        except (ui.UIErr, AttributeError) as e:
            pass
        try:
            # for Chromium-based browsers (if scripting available)
            front_window = window.appscript()
            if tab := getattr(front_window, "active_tab", None):
                return tab.URL()
            return ""
        except:
            return actions.next()

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
