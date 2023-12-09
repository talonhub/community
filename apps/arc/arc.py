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
    def command_palette():
        """Show command palette"""
        actions.key("cmd-l")


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
