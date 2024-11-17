from talon import Context, Module, actions, ui, settings, app

mod = Module()
ctx = Context()
ctx_windows = Context()

mod.apps.microsoft_edge = r"""
os: windows
and app.name: msedge.exe
os: windows
and app.name: Microsoft Edge
os: windows
and app.exe: /^msedge\.exe$/i
os: mac
and app.bundle: com.microsoft.edgemac
os: linux
and app.exe: msedge
"""

ctx.matches = r"""
app: microsoft_edge
"""

ctx_windows.matches = r"""
app: microsoft_edge
os: windows
"""

@ctx.action_class("browser")
class BrowserActions:
    def show_extensions():
        actions.app.tab_open()
        actions.browser.go("edge://extensions")

@ctx.action_class("main")
class MainActions:
    def insert(text):
        actions.next(text)
        # if app.platform == "windows" and ui.focused_element().name in ["Address and search bar", "Find on page"]:
        #     actions.next(text)
        # else:
        #     actions.user.paste(text)
                    