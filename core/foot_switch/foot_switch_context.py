from talon import Context, actions


# ---------- Default non-sleep implementation ----------

ctx_eye_tracker = Context()
ctx_eye_tracker.matches = r"""
tag: user.eye_tracker
tag: user.eye_tracker_frozen
"""


@ctx_eye_tracker.action_class("user")
class EyeTrackerActions:
    def foot_switch_right_down():
        actions.user.mouse_freeze_toggle()

    def foot_switch_right_up(held: bool):
        if held:
            actions.user.mouse_freeze_toggle()


# ---------- Audio conferencing ----------

ctx_voip = Context()
ctx_voip.matches = r"""
mode: command
mode: dictation
mode: sleep
tag: user.voip
"""


@ctx_voip.action_class("user")
class VoipActions:
    def foot_switch_left_down():
        actions.user.mute_microphone()

    def foot_switch_left_up(held: bool):
        if held:
            actions.user.mute_microphone()
