from talon import ctrl, ui, Module, Context, actions, clip, app

mod = Module()
apps = mod.apps
apps.xcode = """
os: mac
and app.name: Xcode
"""

ctx = Context()
ctx.matches = r"""
app: xcode
"""


@ctx.action_class("edit")
class edit_actions:
    def jump_line(n: int):
        actions.key("cmd-l")
        actions.sleep("100ms")
        actions.insert(str(n))
        actions.key("enter")
