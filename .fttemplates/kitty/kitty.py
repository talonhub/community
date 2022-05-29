from talon import Context, actions, ui, Module, app, clip

mod = Module()

mod.apps.kitty = """
app.name: FTName
"""

mod.apps.kitty = """
os: mac
and app.bundle: net.kovidgoyal.kitty
"""

ctx = Context()
ctx.matches = r"""
app: kitty
"""


def ckey():
    return "cmd" if app.platform == "mac" else f"{ckey()}"


def on_mac():
    return app.platform == "mac"


@ctx.action_class("user")
class user_actions:
    def tab_jump(number: int):
        if number < 0 or number > 9:
            raise RuntimeError(f"number should be in range 1-9")
        actions.key(f"{ckey()}-{number}")


@ctx.action_class("edit")
class edit_actions:
    def page_down():
        actions.key("shift-pagedown")

    def find(text: str):
        actions.key(f"{ckey()}-shift-f")
        actions.insert(text)

    def page_up():
        # print(100 * "fsdafs\n")
        actions.key("shift-pageup")

    def paste():
        if on_mac():
            actions.key(f"{ckey()}-v")
        else:
            actions.key(f"{ckey()}-shift-v")

    def copy():
        if on_mac():
            actions.key(f"{ckey()}-c")
        else:
            actions.key(f"{ckey()}-shift-c")


@ctx.action_class("app")
class user_actions:
    def tab_next():
        actions.key(f"{ckey()}-pagedown")

    def tab_open():
        if on_mac():
            actions.key(f"{ckey()}-t")
        else:
            actions.key(f"{ckey()}-shift-t")

    def tab_close():
        if on_mac():
            actions.key(f"{ckey()}-w")
        else:
            actions.key(f"{ckey()}-shift-w")

    def tab_previous():
        actions.key(f"{ckey()}-pageup")
