import string
from talon import Context, actions

visual_studio_ctx= Context()

visual_studio_ctx.matches = r"""
app: visual_studio
"""

@visual_studio_ctx.action_class("user")
class VisualStudioActions:
  def directory() -> string:
    return "visual-studio-commandServer"

  def emit_pre_phrase_signal() -> bool:
    print("****Visual studio pre-phrase***")
    return actions.user.live_pre_phrase_signal()