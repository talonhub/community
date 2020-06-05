os: windows
os: linux
app: Slack
app: slack.exe
#todo: some sort of plugin, consolidate with teams or something?
-
# Workspaces
workspace <number>: key("ctrl-{number}")
previous workspace: key(ctrl-shift-tab)
next workspace: key(ctrl-tab)
# Channel
channel: key(ctrl-k)
channel <user.text>:
    key(ctrl-k)
    insert(user.formatted_text(user.text, "ALL_LOWERCASE"))
([channel] unread last | gopreev): key(alt-shift-up)
([channel] unread next | goneck): key(alt-shift-down)
(slack | lack) [channel] info: key(ctrl-shift-i)
channel up: key(alt-up)
channel down: key(alt-down)
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
(slack | lack) (find | search): key(ctrl-f)
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
mark all read: key(shift-esc)
mark channel read: key(esc)
(clear | scrap | scratch): key(ctrl-a backspace)
    # Files and Snippets
(slack | lack) upload: key(ctrl-u)
(slack | lack) snippet: key(ctrl-shift-enter)
    # Calls
([toggle] mute | unmute): key(m)
(slack | lack) ([toggle] video): key(v)
(slack | lack) invite: key(a)
    # Miscellaneous
(slack | lack) shortcuts: key(ctrl-/)
emote <user.text>: "{text}"
