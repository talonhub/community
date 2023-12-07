from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

mod.apps.arc = "app.name: Arc"
mod.apps.arc = """
os: mac
app.bundle: company.thebrowser.Browser

"""
ctx.matches = r"""
app: arc
"""


@mod.action_class
class Actions:
    def arc_mod(key: str):
        """Press the specified key with the correct modifier key for the OS"""
        if app.platform == "mac":
            actions.key(f"cmd-{key}")
        else:
            actions.key(f"ctrl-{key}")


@ctx.action_class("user")
class UserActions:
    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()


@ctx.action_class("browser")
class BrowserActions:
    def show_extensions():
        actions.app.tab_open()
        actions.browser.go("arc://extensions")
