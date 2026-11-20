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
[channel] unread last | gopreev: user.messaging_unread_previous()
[channel] unread next | goneck: user.messaging_unread_next()
go (find | search): user.messaging_open_search()
mark (all | workspace | server) read: user.messaging_mark_workspace_read()
mark channel read: user.messaging_mark_channel_read()
upload file: user.messaging_upload_file()

# Contacts
new message: user.messaging_open_new_message()
message {user.contact_full_names}: user.messaging_message_contact(contact_full_names)
message from {user.contact_full_names}:
    user.messaging_search_messages_from(contact_full_names)
# provide both anchored and unanchored commands via 'over'
text {user.contact_full_names} <user.text>$:
    user.messaging_message_contact(contact_full_names)
    insert(text)
text {user.contact_full_names} <user.text> {user.phrase_ender}:
    user.messaging_message_contact(contact_full_names)
    insert("{text}{phrase_ender}")
