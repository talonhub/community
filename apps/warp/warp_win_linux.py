from talon import Context, Module, actions

mod = Module()

mod.apps.warp = """
os: linux
and app.name: warp
"""
mod.apps.warp = """
os: windows
and app.exe: warp.exe
"""

ctx = Context()
ctx.matches = r"""
os: linux
os: windows
app: warp
"""


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_close():
        actions.key("ctrl-shift-w")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"ctrl-{number}")

    def tab_final():
        actions.key("ctrl-9")


@ctx.action_class("edit")
class EditActions:
    def word_left():
        actions.key("ctrl-left")

    def word_right():
        actions.key("ctrl-right")
