# meet.py
from talon import Module, Context, ctrl, actions
mod = Module()
ctx = Context()

@mod.action_class
class GoogleMeetActions:
    def toggle_meet_and_talon():
        """
        toggle microphone mute for google meet and talon
        """
        # access meet
        app = actions.user.get_running_app("google meet")

        # focus first tab
        ctrl.key_press("d", app=app, cmd=True)
        if not actions.speech.enabled():
            actions.speech.enable()
        else:
            actions.speech.disable()

    def toggle_microphone():
        """toggle google meet microphone"""
        actions.key("cmd-d")

    def toggle_camera():
        """toggle google meet camera"""
        actions.key("cmd-e")

    def toggle_chat():
        """toggle google meet chat"""
        actions.key("cmd-ctrl-c")

    def toggle_people():
        """toggle google meet people"""
        actions.key("cmd-ctrl-p")

    def toggle_captions():
        """toggle google meet captions"""
        actions.key("c")

    def toggle_hand():
        """toggle google meet hand"""
        actions.key("cmd-ctrl-h")

    def leave_meeting():
        """leave google meet meeting"""
        actions.key("cmd-left")