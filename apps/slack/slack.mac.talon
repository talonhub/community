os: mac
app: slack
-
tag(): user.messaging
# Workspace
workspace <number>: key("cmd-{number}")
# Channel
[channel] info: key(cmd-shift-i)
# Navigation
(move | next) focus: key(ctrl-`)
[next] (section | zone): key(f6)
(previous | last) (section | zone): key(shift-f6)
[direct] messages: key(cmd-shift-k)
threads: key(cmd-shift-t)
[next] (element | bit): key(tab)
(previous | last) (element | bit): key(shift-tab)
(my stuff | activity): key(cmd-shift-m)
directory: key(cmd-shift-e)
(starred [items] | stars): key(cmd-shift-s)
unread [messages]: key(cmd-j)
(go | undo | toggle) full: key(ctrl-cmd-f)
grab left: key(shift-up)
grab right: key(shift-down)
add line: key(shift-enter)
(slap | slaw | slapper): key(cmd-right shift-enter)
(react | reaction): key(cmd-shift-\\)
(insert command | commandify): key(cmd-shift-c)

insert code:
    insert("```")
    
(bull | bullet | bulleted) [list]: key(cmd-shift-8)
(number | numbered) [list]: key(cmd-shift-7)
(quotes | quotation): key(cmd-shift->)
bold: key(cmd-b)
(italic | italicize): key(cmd-i)
(strike | strikethrough): key(cmd-shift-x)
(clear | scrap | scratch): key(cmd-a backspace)
snippet: key(cmd-shift-enter)
# Calls
([toggle] mute | unmute): key(m)
([toggle] video): key(v)
invite: key(a)
# Miscellaneous
shortcuts: key(cmd-/)
emote <user.text>: "{text}"
toggle left sidebar: key(cmd-shift-d)
toggle right sidebar: key(cmd-.)

###############################################################################
### maciek
###############################################################################

back: key(cmd-[)
front: key(cmd-])

[go] channel <user.text>:
    user.messaging_open_channel_picker()
    insert(user.formatted_text(user.text, "ALL_LOWERCASE"))

pop channel <user.text>:
    user.messaging_open_channel_picker()
    insert(user.formatted_text(user.text, "ALL_LOWERCASE"))
    sleep(100ms)
    key(enter)
    
