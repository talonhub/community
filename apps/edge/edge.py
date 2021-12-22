from talon import ctrl, ui, Module, Context, actions, clip, app

mod = Module()
ctx = Context()

mod.apps.microsoft_edge = """
os: windows
and app.name: msedge.exe
os: windows
and app.name: Microsoft Edge
os: windows
and app.exe: msedge.exe
os: mac
and app.bundle: com.microsoft.edgemac
"""

ctx.matches = r"""
app: microsoft_edge
"""


@ctx.action_class("browser")
class BrowserActions:
    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("enter")
