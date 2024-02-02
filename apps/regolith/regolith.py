from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
os: linux
tag: user.regolith
"""

mod.tag("regolith", desc="Toggle for Regolith desktop environment")


@ctx.action_class("user")
class Actions:
    def desktop(number: int):
        actions.key(f"super-{number}")

    def window_move_desktop(desktop_number: int):
        actions.key(f"super-shift-{desktop_number}")
