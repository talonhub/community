from talon import Context, actions

ctx = Context()

# i don't see a need to restrict the app here, this just defines the actions
# each app can support appropriate voice commands as needed
# the below are for 1password, redefine as needed
ctx.matches = r"""
os: mac
"""


@ctx.action_class("user")
class UserActions:
    def password_fill():
        actions.key("cmd-\\")

    def password_show():
        actions.key("cmd-alt-\\")

    def password_new():
        actions.key("cmd-i")

    def password_duplicate():
        actions.key("cmd-d")

    def password_edit():
        actions.key("cmd-e")

    def password_delete():
        actions.key("cmd-backspace")
