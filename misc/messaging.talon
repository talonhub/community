tag: user.messaging
-
# Navigation
previous (workspace | server): user.messaging_workspace_previous()
next (workspace | server): user.messaging_workspace_next()
channel: user.messaging_open_channel_picker()
channel <user.text>:
    user.messaging_open_channel_picker()
    insert(user.formatted_text(user.text, "ALL_LOWERCASE"))
channel up: user.messaging_channel_previous()
channel down: user.messaging_channel_next()
([channel] unread last | gopreev): user.messaging_unread_previous()
([channel] unread next | goneck): user.messaging_unread_next()
go (find | search): user.messaging_open_search()
mark (all | workspace | server) read: user.messaging_mark_workspace_read()
mark channel read: user.messaging_mark_channel_read()
upload file: user.messaging_upload_file()
