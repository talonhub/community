from talon import Context, Module, actions, app

ctx = Context()
mod = Module()
apps = mod.apps
apps.firefox = "app.name: Firefox"
apps.firefox = "app.name: Firefox Developer Edition"
apps.firefox = "app.name: firefox"
apps.firefox = """
os: windows
and app.name: Firefox
os: windows
and app.exe: firefox.exe
"""
apps.firefox = """
os: mac
and app.bundle: org.mozilla.firefox
"""

ctx.matches = r"""
app: firefox
"""

cmd_ctrl = "cmd" if app.platform == "mac" else "ctrl"


@ctx.action_class("user")
class UserActions:
    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()


@ctx.action_class("browser")
class BrowserActions:
    def bookmarks():
        if app.platform == "mac":
            actions.key("cmd-shift-o")
        else:
            actions.key("ctrl-shift-b")

    def bookmarks_bar():
        actions.key(f"{cmd_ctrl}-b")

    def go_home():
        actions.key("alt-home")

    def open_private_window():
        actions.key(f"{cmd_ctrl}-shift-p")

    def show_downloads():
        if app.platform == "linux":
            actions.key("ctrl-shift-y")
        else:
            actions.key(f"{cmd_ctrl}-j")

    def show_extensions():
        actions.key(f"{cmd_ctrl}-shift-a")
