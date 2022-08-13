import string
from talon import Context,  actions

vs_code_ctx = Context()

vs_code_ctx.matches = r"""
app: vscode
"""

@vs_code_ctx.action_class("user")
class VsCodeAction:
  def directory() -> string: 
    return "vscode-command-server"

  def emit_pre_phrase_signal() -> bool:
    return actions.user.live_pre_phrase_signal()  

  def command_client_fallback(command_id: str):
    """Execute command via command palette. Preserves the clipboard."""
    actions.user.command_palette()
    actions.user.paste(command_id)
    actions.key("enter")

  def vscode(command_id: str):
          """Execute command via vscode command server, if available, or fallback
          to command palette."""
          actions.user.post_command(command_id)