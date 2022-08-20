import string

from talon import Context, actions

ctx = Context()

ctx.matches = r"""
app: visual_studio
"""

ctx.tags = ["user.command_client"]


@ctx.action_class("user")
class VisualStudioActions:
    def command_server_directory() -> string:
        return "visual-studio-commandServer"
