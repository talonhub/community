from talon import Context, Module, actions

mod = Module()
ctx = Context()

apps = mod.apps
apps.meld = """
os: windows
and app.name: Visual diff and merge tool
os: windows
and app.exe: meld.exe
"""

ctx.matches = r"""
app: meld
"""


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.key("ctrl-n")

    def tab_previous():
        actions.key("ctrl-alt-pageup")

    def tab_next():
        actions.key("ctrl-alt-pagedown")

    def tab_reopen():
        print("Meld does not support this action.")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number):
        if number < 10:
            actions.key(f"alt-{number}")

    def tab_final():
        print("Meld does not support this action.")

    def tab_duplicate():
        print("Meld does not support this action.")
