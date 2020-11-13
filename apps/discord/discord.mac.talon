os: mac
app: discord
-
tag(): user.messaging

# Navigation: Servers
action(user.messaging_workspace_previous): key(cmd-alt-up)
action(user.messaging_workspace_next): key(cmd-alt-down)

# Navigation: Channels
action(user.messaging_open_channel_picker): key(cmd-k)
action(user.messaging_channel_previous): key(alt-up)
action(user.messaging_channel_next): key(alt-down)
action(user.messaging_unread_previous): key(alt-shift-up)
action(user.messaging_unread_next): key(alt-shift-down)
action(user.discord_mentions_last): key(cmd-alt-shift-up)
action(user.discord_mentions_next): key(cmd-alt-shift-down)
action(user.discord_oldest_unread): key(shift-paegup)

# UI
action(user.discord_toggle_pins): key(cmd-p)
action(user.discord_toggle_inbox): key(cmd-i)
action(user.discord_toggle_members): key(cmd-u)
action(user.discord_emoji_picker): key(cmd-e)
action(user.discord_gif_picker): key(cmd-g)

# Misc
action(user.messaging_mark_workspace_read): key(shift-esc)
action(user.messaging_mark_channel_read): key(esc)
action(user.messaging_upload_file): key(cmd-shift-u)
action(user.discord_mark_inbox_read): key(cmd-shift-e)
action(user.discord_mute): key(cmd-shift-m)
action(user.discord_deafen): key(cmd-shift-d)
action(user.discord_answer_call): key(cmd-enter)
action(user.discord_decline_call): key(esc)
