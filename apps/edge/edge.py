from talon import Context, Module, actions

mod = Module()
ctx = Context()

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


@ctx.action_class("browser")
class BrowserActions:
    def show_extensions():
        actions.app.tab_open()
        actions.browser.go("edge://extensions")
