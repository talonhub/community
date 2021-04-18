app: things3
-
tag(): user.todo_list

new task: key(cmd-n)
action(user.mark_complete): key(cmd-.)
action(user.mark_cancelled): key(cmd-alt-.)

action(user.show_inbox): key(cmd-1)
action(user.show_today): key(cmd-2)
action(user.show_upcoming): key(cmd-3)
action(user.show_anytime): key(cmd-4)
action(user.show_someday): key(cmd-5)
action(user.show_logbook): key(cmd-6)
show tag {user.things_tag}: user.show_tag(things_tag)
show list {user.things_project}: user.show_things_list(things_project)

follow link: key(cmd-alt-enter)

tag this <user.things_tags>: user.tag_todo(things_tags)
move this [to] {user.things_project}: user.move_todo(things_project)
move this [to] inbox: user.move_todo("Inbox")

do this today: key(cmd-t)
do this evening: key(cmd-e)
do this (anytime | any time): key(cmd-r)
do this someday: key(cmd-o)
do this <user.text>:
    key(cmd-s)
    insert(text)
    key(enter)

deadline <user.text>:
    key(cmd-shift-d)
    insert(text)
    key(enter)

clear deadline:
    key(cmd-shift-d backspace enter)

filter [tag] <user.things_tags>: user.filter_by_tag(things_tags)
clear filter: key(ctrl-escape)

action(user.dental_click): key(cmd-enter)

add checklist: key(cmd-shift-c)

drag [this] way up: key(cmd-alt-up)
drag [this] way down: key(cmd-alt-down)
drag [this] up: key(cmd-up)
drag [this] down: key(cmd-down)