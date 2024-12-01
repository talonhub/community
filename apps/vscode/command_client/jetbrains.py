from talon import Context

ctx = Context()

ctx.matches = r"""
app: jetbrains
"""

ctx.tags = ["user.command_client"]

@ctx.action_class("user")
class JetbrainsActions:
    def command_server_directory() -> str:
        return "jetbrains-command-server"
