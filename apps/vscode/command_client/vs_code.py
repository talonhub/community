import string

from talon import Context, actions

ctx = Context()

ctx.matches = r"""
app: vscode
"""
ctx.tags = ["user.command_client"]


@ctx.action_class("user")
class VsCodeAction:
    def command_server_directory() -> string:
        return "vscode-command-server"

    def emit_pre_phrase_signal() -> bool:
        return actions.user.live_pre_phrase_signal()

    def command_client_fallback(command_id: str):
        """Execute command via command palette. Preserves the clipboard."""
        actions.user.command_palette()
        actions.user.paste(command_id)
        actions.key("enter")

   