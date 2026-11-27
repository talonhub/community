from talon import Module

mod = Module()
mod.tag("messaging", desc="Tag for generic multi-channel messaging apps")
mod.setting(
    "messaging_contact_delay",
    type=int,
    default=400,
    desc="Milliseconds to wait for dialogs to open when messaging or searching a contact",
)


@mod.action_class
class messaging_actions:
    # Navigation and UI components

    def messaging_workspace_previous():
        """Move to previous workspace/server"""

    def messaging_workspace_next():
        """Move to next workspace/server"""

    def messaging_open_channel_picker():
        """Open channel picker"""

    def messaging_channel_previous():
        """Move to previous channel"""

    def messaging_channel_next():
        """Move to next channel"""

    def messaging_unread_previous():
        """Move to previous unread channel"""

    def messaging_unread_next():
        """Moved to next unread channel"""

    def messaging_open_search():
        """Open message search"""

    def messaging_mark_workspace_read():
        """Mark this workspace/server as read"""

    def messaging_mark_channel_read():
        """Mark this channel as read."""

    def messaging_upload_file():
        """Upload a file as a message"""

    # Contacts

    def messaging_open_new_message():
        """Open a new message"""

    def messaging_message_contact(name: str):
        """Open a direct message to the given person"""

    def messaging_search_messages_from(name: str):
        """Search for messages sent by the given person"""
