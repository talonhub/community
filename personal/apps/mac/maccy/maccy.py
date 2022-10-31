from talon import ui, Module, Context, registry, actions, imgui, cron
mod = Module()
mod.apps.maccy = """
os: mac
and app.bundle: org.p0deje.Maccy
"""
ctx_mac = Context()
ctx_mac.matches = r"""
app: maccy
"""


@ctx_mac.action_class("user")
class UserActionsMac:
    def pick(number: int):
        actions.key(f"down:{number - 1} enter")
