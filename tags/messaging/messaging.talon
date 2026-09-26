tag: user.messaging
-

# Navigation
next (workspace | server): user.messaging_workspace_next()
(previous | prev) (workspace | server): user.messaging_workspace_previous()
channel: user.messaging_open_channel_picker()
channel <user.text>:
    user.messaging_open_channel_picker()
    insert(user.formatted_text(user.text, "ALL_LOWERCASE"))
channel up: user.messaging_channel_previous()
channel down: user.messaging_channel_next()
[channel] unread next | goneck: user.messaging_unread_next()
[channel] unread (previous | prev) | gopreev: user.messaging_unread_previous()
go (find | search): user.messaging_open_search()
mark (all | workspace | server) read: user.messaging_mark_workspace_read()
mark channel read: user.messaging_mark_channel_read()
upload file: user.messaging_upload_file()
