app: discord
-
tag(): user.messaging
tag(): user.emoji

# Navigation: Channels
[channel] mentions last: user.discord_mentions_last()
[channel] mentions next: user.discord_mentions_next()
oldest unread: user.discord_oldest_unread()
{user.discord_destination} [<user.text>]:
    user.discord_quick_switcher(user.discord_destination, user.text or "")
switcher: user.discord_quick_switcher("", "")
current call: user.discord_go_current_call()
toggle (dee ems | dims): user.discord_toggle_dms()

# UI
toggle pins: user.discord_toggle_pins()
toggle inbox: user.discord_toggle_inbox()
toggle (members | member list): user.discord_toggle_members()
pick emoji: user.discord_emoji_picker()
pick (jif | gif | gift): user.discord_gif_picker()

# Misc
mark inbox channel read: user.discord_mark_inbox_read()
[toggle] (mute | unmute): user.discord_mute()
(mute | unmute) and sleep:
    user.discord_mute()
    speech.disable()
[toggle] (deafen | undeafen): user.discord_deafen()
answer call: user.discord_answer_call()
decline call: user.discord_decline_call()
