from talon import Context, Module, actions

# --- App definition ---
mod = Module()
mod.apps.atril = """
os: linux
and app.name: Atril
"""

# Context matching
ctx = Context()
ctx.matches = r"""
app: atril
"""


# --- Implement actions ---
@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_current():
        actions.key("ctrl-l")
        page = actions.edit.selected_text()
        actions.key("right escape")
        return int(page)

    def page_next():
        actions.key("ctrl-pagedown")

    def page_previous():
        actions.key("ctrl-pageup")

    def page_jump(number: int):
        actions.key("ctrl-l")
        actions.insert(str(number))
        actions.key("enter")

    def page_final():
        actions.key("ctrl-end")
