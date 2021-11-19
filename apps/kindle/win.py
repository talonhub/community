from talon import Context, actions

# Context matching
ctx = Context()
ctx.matches = """
os: windows
app: kindle
"""


# --- Implement actions ---
@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_next(): actions.key("down")
    def page_previous(): actions.key("up")
    def page_jump(number: int):
        actions.key("ctrl-g")
        actions.insert(str(number))
        actions.key("enter")
