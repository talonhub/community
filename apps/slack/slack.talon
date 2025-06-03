app: slack
-
tag(): user.messaging
tag(): user.emoji
# Workspace
workspace <number>: user.slack_open_workspace(number)
# Channel
(slack | lack) [channel] info: user.slack_show_channel_info()

(section | zone) [next]: user.slack_section_next()
(section | zone) (previous | last): user.slack_section_previous()
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