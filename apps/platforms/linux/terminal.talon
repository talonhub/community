os: linux
tag: terminal
-
tag(): user.file_manager
run last:
    key(up)
    key(enter)
rerun <user.text>:
    key(ctrl-r)
    insert(text)
rerun search:
    key(ctrl-r)
kill all:
    key(ctrl-c)
    
    # XXX - these are specific to certain terminals only and should move into their
    # own <term name>.talon file
go tab <number>:
    key("alt-{number}")
