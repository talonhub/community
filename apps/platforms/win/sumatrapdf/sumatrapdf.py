from talon import Module, Context, actions

# --- App definition ---
mod = Module()
mod.apps.sumatrapdf = """
os: windows
and app.name: SumatraPDF
os: windows
and app.exe: SumatraPDF.exe
"""

# Context matching
ctx = Context()
ctx.matches = """
app: sumatrapdf
"""


# --- Implement actions ---
@ctx.action_class("app")
class app_actions:
    # app.tabs
    def tab_open(): actions.key("ctrl-o")


@ctx.action_class('edit')
class EditActions:
    def zoom_in(): actions.key("+")
    def zoom_out(): actions.key("-")


@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_current():
        actions.key("ctrl-g")
        page = actions.edit.selected_text()
        actions.key("escape")
        return int(page)
    def page_next(): actions.key("n")
    def page_previous(): actions.key("p")
    def page_jump(number: int):
        actions.key("ctrl-g")
        actions.insert(str(number))
        actions.key("enter")
    def page_final(): actions.key("end")
    # user.tabs
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"alt-{number}")
    def tab_final(): actions.key("alt-9")
