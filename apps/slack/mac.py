from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app: slack
"""


@ctx.action_class("user")
class UserActions:
    def messaging_workspace_previous():
        actions.key("cmd-shift-[")

    def messaging_workspace_next():
        actions.key("cmd-shift-]")

    def messaging_open_channel_picker():
        actions.key("cmd-k")

    def messaging_channel_previous():
        actions.key("alt-up")

    def messaging_channel_next():
        actions.key("alt-down")

    def messaging_unread_previous():
        actions.key("alt-shift-up")

    def messaging_unread_next():
        actions.key("alt-shift-down")

    def messaging_open_search():
        actions.key("cmd-f")

    def messaging_mark_workspace_read():
        actions.key("shift-esc")

    def messaging_mark_channel_read():
        actions.key("esc")

    # Files and Snippets
    def messaging_upload_file():
        actions.key("cmd-u")
