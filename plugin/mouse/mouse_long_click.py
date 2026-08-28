from talon import Context, Module, ctrl

mod = Module()

mod.tag(
    "mouse_long_click",
    desc="Tag for enabling long click behavior",
)

ctx = Context()
ctx.matches = r"""
tag: user.mouse_long_click
"""


@ctx.action_class("main")
class MainActions:
    @staticmethod
    def mouse_click(button: int = 0):
        ctrl.mouse_click(button=button, hold=16000)
