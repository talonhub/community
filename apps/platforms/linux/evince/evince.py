from talon import Module, Context, actions

# --- App definition ---
mod = Module()
mod.apps.evince = """
os: linux
and app.name: Evince
"""

# Context matching
ctx = Context()
ctx.matches = r"""
app: evince
"""


# --- Implement actions ---
@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_current():
        actions.key("ctrl-l")
        page = actions.edit.selected_text()
        actions.key("escape")
        return int(page)
    def page_next(): actions.key("n")
    def page_previous(): actions.key("p")
    def page_jump(number: int):
        actions.key("ctrl-l")
        actions.insert(str(number))
        actions.key("enter")
    def page_final(): actions.key("ctrl-end")
