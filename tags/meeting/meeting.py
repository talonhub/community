from talon import Context, Module, ui

mod = Module()
mod.tag("meeting", desc="Tag to indicate that the user is in a meeting")

global_ctx = Context()


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

    def meeting_started(app: str, window: ui.Window):
        """A meeting has started in the specified app and window"""
        global_ctx.tags |= {"user.meeting_" + app}

    def meeting_ended(app: str, window: ui.Window):
        """A meeting has started in the specified app and window"""
        global_ctx.tags -= {"user.meeting_" + app}
