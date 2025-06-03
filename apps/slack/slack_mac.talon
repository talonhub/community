os: mac
app: slack
-
# Navigation
focus (move | next): key(ctrl-`)

(slack | lack) (starred [items] | stars): key(cmd-shift-s)
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
