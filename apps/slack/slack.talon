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