app: things3
-
tag(): user.todo_list

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
do this (anytime | any time): key(cmd-r)
do this someday: key(cmd-o)
do this <user.text>:
    key(cmd-s)
    insert(text)

filter [tag] <user.things_tags_with_shortcut>: user.filter_by_tag(things_tags_with_shortcut)
filter clear: key(ctrl-escape)