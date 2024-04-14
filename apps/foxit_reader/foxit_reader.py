from talon import Context, Module, actions

mod = Module()
ctx = Context()

# --- App definition ---
mod.apps.foxit_reader = r"""
os: windows
and app.name: /^Foxit Reader/
os: windows
and app.exe: /^foxitreader\.exe$/i
os: windows
and app.name: Foxit PDF Reader
os: windows
and app.exe: /^foxitpdfreader\.exe$/i
"""
# Context matching
ctx.matches = """
app: foxit_reader
"""


@ctx.action_class("app")
class AppActions:
    # app.tabs
    def tab_open():
        actions.key("ctrl-o")

    def tab_reopen():
        actions.app.notify("Foxit does not support this action.")


@ctx.action_class("user")
class UserActions:
    # user.tabs
    def tab_jump(number):
        actions.app.notify("Foxit does not support this action.")

    def tab_final():
        actions.app.notify("Foxit does not support this action.")

    def tab_duplicate():
        actions.app.notify("Foxit does not support this action.")

    # user.pages
    def page_current() -> int:
        actions.key("ctrl-g")
        page = actions.edit.selected_text()
        return int(page)

    def page_next():
        actions.key("right")

    def page_previous():
        actions.key("left")

    def page_jump(number: int):
        actions.key("ctrl-g")
        actions.insert(str(number))
        actions.key("enter")

    def page_final():
        # actions.key("fn-right")
        actions.key("end")
