from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app: discord
"""


@ctx.action_class("user")
class UserActions:
    # Navigation: QuickSwitcher
    def discord_quick_switcher(dest_type: str, dest_search: str):
        actions.key("cmd-k")
        actions.insert(dest_type)
        if dest_search:
            actions.insert(dest_search)

    # Navigation: Servers
    def messaging_workspace_previous():
        actions.key("cmd-alt-up")

    def messaging_workspace_next():
        actions.key("cmd-alt-down")

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
        actions.key("cmd-alt-shift-up")

    def discord_mentions_next():
        actions.key("cmd-alt-shift-down")

    def discord_oldest_unread():
        actions.key("shift-pageup")

    # UI
    def discord_toggle_pins():
        actions.key("cmd-p")

    def discord_toggle_inbox():
        actions.key("cmd-i")

    def discord_toggle_members():
        actions.key("cmd-u")

    def discord_emoji_picker():
        actions.key("cmd-e")

    def discord_gif_picker():
        actions.key("cmd-g")

    def discord_sticker_picker():
        actions.key("cmd-s")

    # Misc
    def messaging_mark_workspace_read():
        actions.key("shift-esc")

    def messaging_mark_channel_read():
        actions.key("esc")

    def messaging_upload_file():
        actions.key("cmd-shift-u")

    def discord_mark_inbox_read():
        actions.key("cmd-shift-e")

    def discord_mute():
        actions.key("cmd-shift-m")

    def discord_deafen():
        actions.key("cmd-shift-d")

    def discord_answer_call():
        actions.key("cmd-enter")

    def discord_decline_call():
        actions.key("esc")

    def discord_go_current_call():
        actions.key("cmd-alt-a")

    def discord_toggle_dms():
        actions.key("cmd-alt-right")
