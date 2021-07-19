os: mac
app: obsidian
#todo: some sort of plugin, consolidate with teams or something?
-
#It would be nice to have  one file both for linux and mac.
go search [<user.text>]$: 
    key(cmd-u)
    sleep(50ms)
    insert(text or "")
bullet: insert("- ")
open [<user.text>]$: 
    key(cmd-o)
    sleep(50ms)
    insert(text or "")

create [<user.text>]$: 
    key(cmd-n)
    sleep(150ms)
    insert(text or "")

please [<user.text>]$: 
    key(cmd-p)
    sleep(50ms)
    insert(text or "")

code insert:
    insert('```\n')
    insert('```')
    key(left left left)
    insert('\n')
    key(up)
    
code line:
    insert('``')
    key(left)

code python:
    insert('```python\n')
    insert('```')
    key(left left left)
    insert('\n')
    key(up)
    
    
create link [<user.text>]: 
    insert("[[")
    insert(text or "")

switch: key(cmd-e)

git sync: key(cmd-shift-k)

backlinks: key(cmd-y)
go back:key(cmd-left)
go front:key(cmd-right)

header one: "# "
header two: "## "
header three: "### "
header four: "#### "
