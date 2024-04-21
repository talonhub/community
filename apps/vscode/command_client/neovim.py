from talon import Context, actions

ctx = Context()

ctx.matches = r"""
app: neovim
"""

ctx.tags = ["user.command_client"]


@ctx.action_class("user")
class VimActions:
    def command_server_directory() -> str:
        return "neovim-command-server"

    def trigger_command_server_command_execution():
        actions.key("ctrl-q")
