from talon import Context, actions

ctx = Context()
ctx.matches = r"""
user.operating_system: windows 10
"""


@ctx.action_class("user")
class Actions:
    def microphone_toggle_video_conference():
        actions.key("super-alt-k")