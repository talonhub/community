from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: windows
os: linux
app: discord
"""

@ctx.action_class('user')
class UserActions:
    # Navigation: Servers
    def messaging_workspace_previous():  actions.key('ctrl-alt-up')
    def messaging_workspace_next():      actions.key('ctrl-alt-down')

    # Navigation: Channels
    def messaging_open_channel_picker(): actions.key('ctrl-k')
    def messaging_channel_previous():    actions.key('alt-up')
    def messaging_channel_next():        actions.key('alt-down')
    def messaging_unread_previous():     actions.key('alt-shift-up')
    def messaging_unread_next():         actions.key('alt-shift-down')
    def discord_mentions_last():         actions.key('ctrl-alt-shift-up')
    def discord_mentions_next():         actions.key('ctrl-alt-shift-down')
    def discord_oldest_unread():         actions.key('shift-paegup')

    # UI
    def discord_toggle_pins():           actions.key('ctrl-p')
    def discord_toggle_inbox():          actions.key('ctrl-i')
    def discord_toggle_members():        actions.key('ctrl-u')
    def discord_emoji_picker():          actions.key('ctrl-e')
    def discord_gif_picker():            actions.key('ctrl-g')

    # Misc
    def messaging_mark_workspace_read(): actions.key('shift-esc')
    def messaging_mark_channel_read():   actions.key('esc')
    def messaging_upload_file():         actions.key('ctrl-shift-u')
    def discord_mark_inbox_read():       actions.key('ctrl-shift-e')
    def discord_mute():                  actions.key('ctrl-shift-m')
    def discord_deafen():                actions.key('ctrl-shift-d')
    def discord_answer_call():           actions.key('ctrl-enter')
    def discord_decline_call():          actions.key('esc')
