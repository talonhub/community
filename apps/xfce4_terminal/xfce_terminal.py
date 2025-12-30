from talon import Context, Module, actions

mod = Module()
mod.apps.xfce4_terminal = """
os: linux
and app.exe: xfce4-terminal
"""

ctx = Context()
ctx.matches = r"""
app: xfce4_terminal
"""


@ctx.action_class("user")
class user_actions:
    def tab_jump(number):
        actions.key(f"alt-{number}")


@ctx.action_class("app")
class app_actions:
    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_previous():
        actions.key("ctrl-pageup")

    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_close():
        actions.key("ctrl-shift-w")

    def window_open():
        actions.key("ctrl-shift-n")

    def window_close():
        actions.key("ctrl-shift-q")


@ctx.action_class("edit")
class EditActions:
    def page_down():
        actions.key("shift-pagedown")

    def page_up():
        actions.key("shift-pageup")

    def paste():
        actions.key("ctrl-shift-v")

    def copy():
        actions.key("ctrl-shift-c")

    def file_end():
        actions.key("shift-end")

    def file_start():
        actions.key("shift-home")

    def find(text: str = None):
        actions.key("ctrl-shift-f")
        if text:
            actions.insert(text)

    def delete_line():
        actions.edit.line_start()
        actions.key("ctrl-k")

    def select_all():
        actions.key("ctrl-shift-a")
