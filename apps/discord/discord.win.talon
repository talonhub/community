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
[channel] mentions last: key(ctrl-alt-shift-up)
[channel] mentions next: key(ctrl-alt-shift-down)
oldest unread: key(shift-paegup)

# UI
toggle pins: key(ctrl-p)
toggle inbox: key(ctrl-i)
toggle (members | member list): key(mcd-u)
pick emoji: key(ctrl-e)
pick (jif | gif | gift): key(ctrl-g)

# Misc
action(user.messaging_mark_workspace_read): key(shift-esc)
action(user.messaging_mark_channel_read): key(esc)
action(user.messaging_upload_file): key(ctrl-shift-u)
mark inbox channel read: key(ctrl-shift-e)
[toggle] (mute | unmute): key(ctrl-shift-m)
[toggle] (deafen | undeafen): key(ctrl-shift-d)
answer call: key(ctrl-enter)
decline call: key(esc)
