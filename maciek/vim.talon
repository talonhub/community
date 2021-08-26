os:mac
mode: user.terminal
mode: command
and tag: terminal
and win.title: /vim/
-
# vim stuff    
quit vim save:
    key(escape)
    insert(":qw!\n")
quit vim:
    key(escape)
    insert(":q!\n")

