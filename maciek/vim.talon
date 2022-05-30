os:mac
mode: user.terminal
mode: command
and tag: terminal
and win.title: /vim/
-
# vim stuff    
vim quit save:
    key(escape)
    insert(":qw!\n")
vim quit:
    key(escape)
    insert(":q!\n")

