tag: user.messaging
-

# Navigation
<user.spatial_previous_next> (workspace | server): user.messaging_workspace_go(spatial_previous_next)
channel: user.messaging_open_channel_picker()
channel <user.text>:
    user.messaging_open_channel_picker()
    insert(user.formatted_text(user.text, "ALL_LOWERCASE"))
channel up: user.messaging_channel_previous()
channel down: user.messaging_channel_next()
[channel] unread <user.spatial_previous_next>: user.messaging_unread_go(spatial_previous_next)
[channel] unread gopreev: user.messaging_unread_go("PREV")
[channel] unread goneck: user.messaging_unread_go("NEXT")
go (find | search): user.messaging_open_search()
mark (all | workspace | server) read: user.messaging_mark_workspace_read()
mark channel read: user.messaging_mark_channel_read()
upload file: user.messaging_upload_file()
