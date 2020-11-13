os: windows
os: linux
app: slack
#todo: some sort of plugin, consolidate with teams or something?
-
tag(): user.messaging
# Workspaces
workspace <number>: key("ctrl-{number}")
action(user.messaging_workspace_previous): key(ctrl-shift-tab)
action(user.messaging_workspace_next): key(ctrl-tab)
# Channel
(slack | lack) [channel] info: key(ctrl-shift-i)
action(user.messaging_open_channel_picker): key(ctrl-k)
action(user.messaging_channel_previous): key(alt-up)
action(user.messaging_channel_next): key(alt-down)
action(user.messaging_unread_previous): key(alt-shift-up)
action(user.messaging_unread_next): key(alt-shift-down)
# Navigation
(move | next) focus: key(ctrl-`)
[next] (section | zone): key(f6)
(previous | last) (section | zone): key(shift-f6)
(slack | lack) [direct] messages: key(ctrl-shift-k)
(slack | lack) threads: key(ctrl-shift-t)
(slack | lack) (history [next] | back | backward): key(alt-left)
(slack | lack) forward: key(alt-right)
[next] (element | bit): key(tab)
(previous | last) (element | bit): key(shift-tab)
(slack | lack) (my stuff | activity): key(ctrl-shift-m)
(slack | lack) directory: key(ctrl-shift-e)
(slack | lack) (starred [items] | stars): key(ctrl-shift-s)
(slack | lack) unread [messages]: key(ctrl-j)
#(go | undo | toggle) full: key(ctrl-cmd-f)
action(user.messaging_open_search): key(ctrl-f)
# Messaging
grab left: key(shift-up)
grab right: key(shift-down)
add line: key(shift-enter)
#"(slack | lack) (slap | slaw | slapper): [key(cmd-right) key(shift-enter")],
(slack | lack) (react | reaction): key(ctrl-shift-\\)
(insert command | commandify): key(ctrl-shift-c)
insert code:
    insert("``````")
    key(left left left)
    key(shift-enter)
    key(shift-enter)
    key(up)
(slack | lack) (bull | bullet | bulleted) [list]: key(ctrl-shift-8)
(slack | lack) (number | numbered) [list]: key(ctrl-shift-7)
(slack | lack) (quotes | quotation): key(ctrl-shift-9)
bold: key(ctrl-b)
(italic | italicize): key(ctrl-i)
(strike | strikethrough): key(ctrl-shift-x)
action(user.messaging_mark_workspace_read): key(shift-esc)
action(user.messaging_mark_channel_read): key(esc)
(clear | scrap | scratch): key(ctrl-a backspace)
    # Files and Snippets
action(user.messaging_upload_file): key(ctrl-u)
(slack | lack) snippet: key(ctrl-shift-enter)
    # Calls
([toggle] mute | unmute): key(m)
(slack | lack) ([toggle] video): key(v)
(slack | lack) invite: key(a)
    # Miscellaneous
(slack | lack) shortcuts: key(ctrl-/)
emote <user.text>: "{text}"
toggle left sidebar: key(ctrl-shift-d)
toggle right sidebar: key(ctrl-.)
