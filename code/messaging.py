from talon import Context, actions, ui, Module, app

mod = Module()
mod.tag("messaging", desc="Tag for generic multi-channel messaging apps")


@mod.action_class
class messaging_actions:
    def messaging_channel_previous():
        """Move to previous channel"""

    def messaging_channel_next():
        """Move to next channel"""

    def messaging_unread_previous():
        """Move to previous unread channel"""

    def messaging_unread_next():
        """Moved to next unread channel"""
