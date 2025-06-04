app: slack
-
tag(): user.messaging
tag(): user.emoji
# Workspace
workspace <number>: user.slack_open_workspace(number)
# Channel
(slack | lack) [channel] info: user.slack_show_channel_info()
focus (move | next): key(ctrl-`)
(section | zone) [next]: user.slack_section_next()
(section | zone) (previous | last): user.slack_section_previous()
(slack | lack) (starred [items] | stars): user.slack_open_starred_items()
(slack | lack) [direct] messages: user.slack_open_direct_messages()
(slack | lack) threads: user.slack_open_threads()
(slack | lack) (history [next] | back | backward): user.slack_go_back()
(slack | lack) forward: user.slack_go_forward()

# Messaging
grab left: key(shift-up)
grab right: key(shift-down)
add line: key(shift-enter)

(slack | lack) (slap | slaw | slapper): edit.line_insert_down()
(element | bit) [next]: key(tab)
(element | bit) (previous | last): key(shift-tab)

(slack | lack) (my stuff | activity): user.slack_open_activity()
(slack | lack) directory: user.slack_open_directory()

(slack | lack) unread [messages]: user.slack_open_unread_messages()

(go | undo | toggle) full: user.slack_toggle_full_screen()
(slack | lack) (react | reaction): user.slack_add_reaction()
(insert command | commandify): user.slack_insert_command()
insert link: user.slack_insert_link()
insert code: user.slack_insert_code()
(slack | lack) (bull | bullet | bulleted) [list]: user.slack_start_bulleted_list()
(slack | lack) (number | numbered) [list]: user.slack_start_numbered_list()
(slack | lack) (quotes | quotation): user.slack_insert_quotation()
bold: user.slack_toggle_bold()
(italic | italicize): user.slack_toggle_italic()
(strike | strikethrough): user.slack_toggle_strikethrough()
(slack | lack) snippet: user.slack_create_snippet()
# Calls
(slack | lack) huddle: user.slack_huddle()
([toggle] mute | unmute): key(m)
(slack | lack) ([toggle] video): key(v)
(slack | lack) invite: key(a)

# Miscellaneous
emote <user.text>: ":{text}:"
(slack | lack) shortcuts: user.slack_open_keyboard_shortcuts()
toggle left sidebar: user.slack_toggle_left_sidebar()
toggle right sidebar: user.slack_toggle_right_sidebar()

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
