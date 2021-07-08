os: mac
app: slack
-
tag(): user.messaging
# Workspace
workspace <number>: key("cmd-{number}")
# Channel
(slack | lack) [channel] info: key(cmd-shift-i)
# Navigation
(move | next) focus: key(ctrl-`)
[next] (section | zone): key(f6)
(previous | last) (section | zone): key(shift-f6)
(slack | lack) [direct] messages: key(cmd-shift-k)
(slack | lack) threads: key(cmd-shift-t)
(slack | lack) (history [next] | back | backward): key(cmd-[)
(slack | lack) forward: key(cmd-])
[next] (element | bit): key(tab)
(previous | last) (element | bit): key(shift-tab)
(slack | lack) (my stuff | activity): key(cmd-shift-m)
(slack | lack) directory: key(cmd-shift-e)
(slack | lack) (starred [items] | stars): key(cmd-shift-s)
(slack | lack) unread [messages]: key(cmd-j)
(go | undo | toggle) full: key(ctrl-cmd-f)
# Messaging
grab left: key(shift-up)
grab right: key(shift-down)
add line: key(shift-enter)
(slack | lack) (slap | slaw | slapper): key(cmd-right shift-enter)
(slack | lack) (react | reaction): key(cmd-shift-\\)
(insert command | commandify): key(cmd-shift-c)
insert code:
    insert("``````")
    key(left left left)
    key(shift-enter)
    key(shift-enter)
    key(up)
(slack | lack) (bull | bullet | bulleted) [list]: key(cmd-shift-8)
(slack | lack) (number | numbered) [list]: key(cmd-shift-7)
(slack | lack) (quotes | quotation): key(cmd-shift->)
bold: key(cmd-b)
(italic | italicize): key(cmd-i)
(strike | strikethrough): key(cmd-shift-x)
(clear | scrap | scratch): key(cmd-a backspace)
(slack | lack) snippet: key(cmd-shift-enter)
# Calls
([toggle] mute | unmute): key(m)
(slack | lack) ([toggle] video): key(v)
(slack | lack) invite: key(a)
# Miscellaneous
(slack | lack) shortcuts: key(cmd-/)
emote <user.text>: "{text}"
toggle left sidebar: key(cmd-shift-d)
toggle right sidebar: key(cmd-.)
