from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

mod.apps.brave = "app.name: Brave Browser"
mod.apps.brave = "app.name: Brave-browser"
mod.apps.brave = r"""
os: windows
and app.exe: /^brave\.exe$/i
os: linux
and app.exe: brave
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
