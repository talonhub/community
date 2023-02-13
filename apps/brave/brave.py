from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

mod.apps.brave = "app.name: Brave Browser"
# TODO: Add other OS application identifiers
mod.apps.brave = """
os: mac
and app.bundle: com.brave.Browser
"""
ctx.matches = r"""
app: brave
"""


@ctx.action_class("user")
class UserActions:
    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()


@ctx.action_class("browser")
class BrowserActions:
    def show_extensions():
        actions.app.tab_open()
        actions.browser.go("brave://extensions")
