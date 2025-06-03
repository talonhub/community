os: mac
app: slack
-
# Navigation
focus (move | next): key(ctrl-`)

(element | bit) [next]: key(tab)
(element | bit) (previous | last): key(shift-tab)
(slack | lack) (my stuff | activity): key(cmd-shift-m)
(slack | lack) directory: key(cmd-shift-e)
(slack | lack) (starred [items] | stars): key(cmd-shift-s)
(slack | lack) unread [messages]: key(cmd-shift-a)
(go | undo | toggle) full: key(ctrl-cmd-f)
(slack | lack) (react | reaction): key(cmd-shift-\)
(insert command | commandify): key(cmd-shift-c)
insert link: key(cmd-shift-u)
insert code: key(cmd-shift-alt-c)
(slack | lack) (bull | bullet | bulleted) [list]: key(cmd-shift-8)
(slack | lack) (number | numbered) [list]: key(cmd-shift-7)
(slack | lack) (quotes | quotation): key(cmd-shift->)
bold: key(cmd-b)
(italic | italicize): key(cmd-i)
(strike | strikethrough): key(cmd-shift-x)
(slack | lack) snippet: key(cmd-shift-enter)
# Calls
([toggle] mute | unmute): key(m)
(slack | lack) huddle: key(cmd-shift-h)
(slack | lack) ([toggle] video): key(v)
(slack | lack) invite: key(a)
# Miscellaneous
(slack | lack) shortcuts: key(cmd-/)
emote <user.text>: "{text}"
toggle left sidebar: key(cmd-shift-d)
toggle right sidebar: key(cmd-.)

# DEPRECATED
(move | next) focus:
    app.notify("please use the voice command 'focus next' instead of 'next focus'")
    key(ctrl-`)
[next] (section | zone):
    app.notify("please use the voice command 'section next' instead of 'next section'")
    key(f6)
(previous | last) (section | zone):
    app.notify("please use the voice command 'section last' instead of 'last section'")
    key(shift-f6)
[next] (element | bit):
    app.notify("please use the voice command 'element next' instead of 'next element'")
    key(tab)
(previous | last) (element | bit):
    app.notify("please use the voice command 'element last' instead of 'last element'")
    key(shift-tab)
