os: windows
os: linux
app: discord
-
tag(): user.messaging

# Navigation: Servers
action(user.messaging_workspace_previous): key(ctrl-alt-up)
action(user.messaging_workspace_next): key(ctrl-alt-down)

# Navigation: Channels
action(user.messaging_open_channel_picker): key(ctrl-k)
action(user.messaging_channel_previous): key(alt-up)
action(user.messaging_channel_next): key(alt-down)
action(user.messaging_unread_previous): key(alt-shift-up)
action(user.messaging_unread_next): key(alt-shift-down)
action(user.discord_mentions_last): key(ctrl-alt-shift-up)
action(user.discord_mentions_next): key(ctrl-alt-shift-down)
action(user.discord_oldest_unread): key(shift-paegup)

# UI
action(user.discord_toggle_pins): key(ctrl-p)
action(user.discord_toggle_inbox): key(ctrl-i)
action(user.discord_toggle_members): key(ctrl-u)
action(user.discord_emoji_picker): key(ctrl-e)
action(user.discord_gif_picker): key(ctrl-g)

# Misc
action(user.messaging_mark_workspace_read): key(shift-esc)
action(user.messaging_mark_channel_read): key(esc)
action(user.messaging_upload_file): key(ctrl-shift-u)
action(user.discord_mark_inbox_read): key(ctrl-shift-e)
action(user.discord_mute): key(ctrl-shift-m)
action(user.discord_deafen): key(ctrl-shift-d)
action(user.discord_answer_call): key(ctrl-enter)
action(user.discord_decline_call): key(esc)
