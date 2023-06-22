from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

mod.apps.chrome = "app.name: Google Chrome"
mod.apps.chrome = """
os: windows
and app.exe: chrome.exe
"""
mod.apps.chrome = """
os: mac
app.bundle: com.google.Chrome
app.bundle: com.google.Chrome.canary
app.bundle: org.chromium.Chromium
"""
mod.apps.chrome = """
os: linux
app.exe: chrome
app.exe: chromium-browser
app.exe: chromium
"""
mod.apps.chrome = """
os: linux
and app.name: Google-chrome
"""

ctx.matches = r"""
app: chrome
"""


@mod.action_class
class Actions:
    def chrome_mod(key: str):
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
        actions.browser.go("chrome://extensions")
