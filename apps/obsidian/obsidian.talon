os: linux
app: obsidian
#todo: some sort of plugin, consolidate with teams or something?
-
go search [<user.text>]: 
    key(ctrl-u)
    sleep(50ms)
    insert(text or "")

open [<user.text>]: 
    key(ctrl-o)
    sleep(50ms)
    insert(text or "")

create [<user.text>]: 
    key(ctrl-n)
    sleep(150ms)
    insert(text or "")
please [<user.text>]: 
    key(ctrl-p)
    sleep(50ms)
    insert(text or "")

    
create link [<user.text>]: 
    insert("[[")
    insert(text or "")

switch: key(ctrl-e)

sync all: key(ctrl-shift-k)

backlinks: key(ctrl-y)
go back:key(alt-left)
go front:key(alt-right)
