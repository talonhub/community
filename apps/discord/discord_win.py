from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: windows
os: linux
app: discord
"""


@ctx.action_class("user")
class UserActions:
    # Navigation: QuickSwitcher
    def discord_quick_switcher(dest_type: str, dest_search: str):
        actions.key("ctrl-k")
        actions.insert(dest_type)
        if dest_search:
            actions.insert(dest_search)

    # Navigation: Servers
    def messaging_workspace_previous():
        actions.key("ctrl-alt-up")

    def messaging_workspace_next():
        actions.key("ctrl-alt-down")

    # Navigation: Channels
    def messaging_channel_previous():
        actions.key("alt-up")

    def messaging_channel_next():
        actions.key("alt-down")

    def messaging_unread_previous():
        actions.key("alt-shift-up")

    def messaging_unread_next():
        actions.key("alt-shift-down")

    def discord_mentions_last():
        actions.key("ctrl-alt-shift-up")

    def discord_mentions_next():
        actions.key("ctrl-alt-shift-down")

    def discord_oldest_unread():
        actions.key("shift-pageup")

    # UI
    def discord_toggle_pins():
        actions.key("ctrl-p")

    def discord_toggle_inbox():
        actions.key("ctrl-i")

    def discord_toggle_members():
        actions.key("ctrl-u")

    def discord_emoji_picker():
        actions.key("ctrl-e")

    def discord_gif_picker():
        actions.key("ctrl-g")

    def discord_sticker_picker():
        actions.key("ctrl-s")

    # Misc
    def messaging_mark_workspace_read():
        actions.key("shift-esc")

    def messaging_mark_channel_read():
        actions.key("esc")

    def messaging_upload_file():
        actions.key("ctrl-shift-u")

    def discord_mark_inbox_read():
        actions.key("ctrl-shift-e")

    def discord_mute():
        actions.key("ctrl-shift-m")

    def discord_deafen():
        actions.key("ctrl-shift-d")

    def discord_answer_call():
        actions.key("ctrl-enter")

    def discord_decline_call():
        actions.key("esc")

    def discord_go_current_call():
        actions.key("ctrl-shift-alt-v")

    def discord_toggle_dms():
        actions.key("ctrl-alt-right")
