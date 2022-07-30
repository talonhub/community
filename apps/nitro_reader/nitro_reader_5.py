from talon import Context, Module, actions

# --- App definition ---
mod = Module()
mod.apps.nitro_reader_five = """
os: windows
and app.name: Nitro Reader 5
os: windows
and app.exe: NitroPDFReader.exe
"""

# Context matching
ctx = Context()
ctx.matches = """
app: nitro_reader_five
"""


# --- Implement actions ---
@ctx.action_class("app")
class app_actions:
    # app.tabs
    def tab_open():
        actions.key("ctrl-shift-o")


@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_next():
        actions.key("right")

    def page_previous():
        actions.key("left")

    def page_jump(number: int):
        actions.key("ctrl-g")
        actions.edit.select_line()
        actions.insert(str(number))
        actions.key("enter alt:2")

    def page_final():
        actions.key("end")
