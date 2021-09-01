os: mac
app: obsidian
#todo: some sort of plugin, consolidate with teams or something?
-
#It would be nice to have  one file both for linux and mac.
go search [<user.text>]$: 
    key(cmd-u)
    sleep(50ms)
    insert(text or "")
bullet: 
    edit.line_start()
    insert("- ")
# bullet: user.obsidian_run_command("Toggle bullet list")

lion [<user.text>]$: 
    key(cmd-o)
    sleep(50ms)
    insert(text or "")

create[note] [<user.text>]$: 
    key(cmd-n)
    sleep(150ms)
    insert(text or "")

please [<user.text>]$: 
    key(cmd-p)
    sleep(50ms)
    insert(text or "")

code block:
    insert('```\n')
    insert('```')
    key(left left left)
    insert('\n')
    key(up)
    # Daily notes:
(daily notes|go daily):
    user.obsidian_run_command("Daily notes:")
anki sync:
    user.obsidian_run_command("Obsidian_to_anki")
go settings:
    user.obsidian_run_command("Open settings")

code line:
    insert('``')
    key(left)

dev tools:
    key(cmd-alt-i)

inspect:
    key(cmd-shift-c)
code python:
    insert('```python\n')
    insert('```')
    key(left left left)
    insert('\n')
    key(up)
    
code typescript:
    insert('```typescript\n')
    insert('```')
    key(left left left)
    insert('\n')
    key(up) 
code css:
    insert('```css\n')
    insert('```')
    key(left left left)
    insert('\n')
    key(up) 

today:
    insert("@Today")
    sleep(50ms)
    key(enter)
tomorrow:
    insert("@tomorrow")
    sleep(50ms)
    key(enter)
    
insert link [<user.text>]: 
    insert("[[")
    insert(text or "")
# end link:
#     insert("]]")


switch: key(cmd-e)

git sync: key(cmd-shift-k)

[show] backlinks: key(cmd-y)
go back:key(cmd-alt-left)
go front:key(cmd-alt-right)
hash tag talon: insert("#talon ")
hash tag code: insert("#vscode ")
hash tag bug: insert("#bug ")
image extra small:
    insert("|#x-small")
    key(escape)
    edit.line_end()

image small:
    insert("|#small")
    key(escape)
    edit.line_end()
    
header one: "# "
header two: "## "
header three: "### "
header four: "#### "
header five: "##### "
header six: "###### "
bold: key(cmd-b)


