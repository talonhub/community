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
[channel] mentions last: key(cmd-alt-shift-up)
[channel] mentions next: key(cmd-alt-shift-down)
oldest unread: key(shift-paegup)

# UI
toggle pins: key(cmd-p)
toggle inbox: key(cmd-i)
toggle (members | member list): key(mcd-u)
pick emoji: key(cmd-e)
pick (jif | gif | gift): key(cmd-g)

# Misc
action(user.messaging_mark_workspace_read): key(shift-esc)
action(user.messaging_mark_channel_read): key(esc)
action(user.messaging_upload_file): key(cmd-shift-u)
mark inbox channel read: key(cmd-shift-e)
[toggle] (mute | unmute): key(cmd-shift-m)
[toggle] (deafen | undeafen): key(cmd-shift-d)
answer call: key(cmd-enter)
decline call: key(esc)
