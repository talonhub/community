# slack.py
from talon import Module, Context, ctrl, actions
mod = Module()
ctx = Context()

@mod.action_class
class SlackHuddleActions:
    def toggle_slack_and_talon():
        """
        toggle microphone mute for slack and talon
        """
        # access meet
        app = actions.user.get_running_app("slack")

        # focus first tab
        ctrl.key_press("space", app=app, cmd=True, shift=True)
        if not actions.speech.enabled():
            actions.speech.enable()
            actions.mode.enable("noise")
        else:
            actions.speech.disable()
            actions.mode.disable("noise")

    def toggle_huddle():
        """toggle google meet microphone"""
        actions.key("cmd-shift-space")

    def leave_huddle():
        """leave google meet meeting"""
        actions.key("cmd-shift-h")