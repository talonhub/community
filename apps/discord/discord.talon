app: discord
-
tag(): user.messaging
tag(): user.emoji
tag(): user.navigation
tag(): user.find

# Messages
# Edit Message: E
# Delete Message: Backspace
# Pin Message: P
# Add Reaction: +
# Reply: R
# Copy Text: CMD+C or Ctrl+C
# Mark Unread: OPT+ENTER
# Focus Text Area: ESC
# Forward Message: F

# Navigation: Messages
go oldest unread: user.discord_channel_oldest_unread()

# Navigation: QuickSwitcher
{user.discord_destination} [<user.text>]:
    user.discord_quick_switcher(user.discord_destination, user.text or "")
switcher: user.discord_quick_switcher("", "")

# Navigation: Channels
[channel] mentions last: user.discord_mentions_last()
[channel] mentions next: user.discord_mentions_next()
oldest unread: user.discord_oldest_unread()
current call: user.discord_go_current_call()

# UI
toggle pins: user.discord_toggle_pins()
toggle inbox: user.discord_toggle_inbox()
toggle (members | member list): user.discord_toggle_members()
toggle (vee see text | voice text): user.discord_toggle_members()
toggle (dee ems | dims): user.discord_toggle_dms()
toggle sound board: user.discord_toggle_soundboard()
pick emoji: user.discord_emoji_picker()
pick (jif | gif | gift): user.discord_gif_picker()
pick sticker: user.discord_sticker_picker()

# Misc
mark inbox channel read: user.discord_mark_inbox_read()
[toggle] (mute | unmute): user.discord_mute()
(mute | unmute) and sleep:
    user.discord_mute()
    speech.disable()
[toggle] (deafen | undeafen): user.discord_deafen()
answer call: user.discord_answer_call()
decline call: user.discord_decline_call()
start call: user.discord_start_call()
(create | join) server: user.discord_create_join_server()
create private group: user.discord_create_private_group()
open support: user.discord_open_support()
start low fie: user.discord_start_lofi()
