from talon import Context, actions

# Context matching
ctx = Context()
ctx.matches = r"""
os: windows
app: thunderbird
"""


# --- Implement actions ---
@ctx.action_class("app")
class AppActions:
    # app.tabs
    def tab_reopen():
        actions.key("ctrl-shift-t")  # only works from inbox tab


@ctx.action_class("user")
class UserActions:
    # user.tabs
    def tab_jump(number: int):
        if number <= 9:
            actions.key(f"ctrl-{number}")

    def tab_final():
        actions.key("ctrl-9")

    # custom actions
    def thunderbird_mod(keys: str):
        actions.key(f"ctrl-{keys}")

    def thunderbird_calendar_view(number: int):
        actions.key(f"alt-{number}")
