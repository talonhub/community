app: windows_terminal
-
tag(): user.tabs
tag(): terminal

settings open : key(ctrl-,)
focus left: key(ctrl-alt-shift-left)
focus right: key(ctrl-alt-shift-right)
focus up: key(ctrl-alt-shift-up)
focus down: key(ctrl-alt-shift-down)
split right: key(alt-shift-=)
split down: key(alt-shift--)
term menu: key(ctrl-shift-f1)

run last: key(up enter)
kill all:
    key(ctrl-c)
    insert("y")
    key(enter)


find it:
    edit.find()

find it <phrase>$:
    # handle consecutive finds by first escaping out of any previous one
    key(escape)
    # make it so
    edit.find("{phrase}\n")
