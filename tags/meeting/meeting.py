from talon import Module

mod = Module()
mod.tag("meeting", desc="Tag to indicate that the user is in a meeting")


@mod.action_class
class meeting_actions:
    def meeting_is_muted() -> bool:
        """Returns whether the current meeting is muted"""
        return False

    def meeting_mute():
        """Mute the current meeting"""

    def meeting_unmute():
        """Unmute the current meeting"""

    def meeting_exit():
        """Exit the current meeting"""
