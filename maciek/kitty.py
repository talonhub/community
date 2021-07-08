from talon import Context, actions, ui, Module, app, clip

mod = Module()
mod.apps.kitty = "app.name: kitty"
ctx = Context()
ctx.matches = r"""
app: kitty
"""


@ctx.action_class("edit")
class edit_actions:
    def page_down():
        actions.key("shift-pagedown")

    def find(text: str):
        actions.key("ctrl-shift-f")
        actions.insert(text)

    def page_up():
        # print(100 * "fsdafs\n")
        actions.key("shift-pageup")

    def paste():
        actions.key("ctrl-shift-v")

    def copy():
        actions.key("ctrl-shift-c")


@ctx.action_class("app")
class user_actions:
    def tab_next():
        actions.key("ctrl-pageup")

    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_close():
        actions.key("ctrl-shift-w")

    def tab_previous():
        actions.key("ctrl-pagedown")
