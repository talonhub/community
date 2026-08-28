from talon import Context, Module, ctrl

mod = Module()

mod.tag(
    "mouse_click_with_hold",
    desc="Hold mouse buttons for 16 ms so clicks register reliably",
)

ctx = Context()
ctx.matches = r"""
tag: user.mouse_click_with_hold
"""


@ctx.action_class("main")
class MainActions:
    @staticmethod
    def mouse_click(button: int = 0):
        ctrl.mouse_click(button=button, hold=16000)
