from talon import Context, Module, actions, ui
from talon.mac import applescript

ctx = Context()
mod = Module()
apps = mod.apps
mod.apps.safari = """
os: mac
and app.bundle: com.apple.Safari
"""

ctx.matches = r"""
app: safari
"""


@ctx.action_class("browser")
class BrowserActions:
    def show_downloads():
        actions.key("cmd-alt-l")

    def show_extensions():
        actions.key("cmd-, tab:8 space")
