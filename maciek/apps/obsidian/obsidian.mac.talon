os: mac
app: obsidian
#todo: some sort of plugin, consolidate with teams or something?
-
#It would be nice to have  one file both for linux and mac.
[go] search [<user.text>]$: 
    key(cmd-u)
    sleep(50ms)
    insert(text or "")
bullet: 
    edit.line_start()
    insert("- ")
# bullet: user.obsidian_run_command("Toggle bullet list")

lion [<user.text>]$:
    key(cmd-p)
    sleep(50ms)
    insert(text or "")

create[note] [<user.text>]$: 
    key(cmd-n)
    sleep(150ms)
    insert(text or "")

please [<user.text>]$: 
    key(alt-p)
    sleep(50ms)
    insert(text or "")

###############################################################################
### code block
###############################################################################
code block:
    insert('```\n')
code block sql:
    insert('```sql\n')
code block python:
    insert('```python\n')
code block typescript:
    insert('```typescript\n')
code block css:
    insert('```css\n')


# Daily notes:
daily show:
    user.obsidian_run_command("daily today daily")
anki sync:
    user.obsidian_run_command("Obsidian_to_anki")
settings go:
    user.obsidian_run_command("Open settings")

code insert:
    insert('``')
    key(left)

dev tools:
    key(cmd-alt-i)

inspect:
    key(cmd-shift-c)
    




    
# Inserting stuff    
# because link is very similar to ink, I added 'create' to the front.
create link [<user.text>]: 
    insert("[[")
    insert(text or "")
insert time:
    insert(" /time")
    sleep(50ms)
    key(enter)
    
today:
    insert("@Today")
    sleep(50ms)
    key(enter)
tomorrow:
    insert("@tomorrow")
    sleep(50ms)
    key(enter)
yesterday:
    insert("@yesterday")
    sleep(50ms)
    key(enter)
# end link:
#     insert("]]")



switch: key(cmd-e)

git sync: key(cmd-shift-k)

[show] backlinks: key(cmd-y)
go back:key(cmd-alt-left)
go front:key(cmd-alt-right)

# TODO: tranche to talon lists
hash tag talon: insert("#talon ")
hash tag code: insert("#vscode ")
hash tag bug: insert("#bug ")


# image extra small:
#     insert("|#x-small")
#     key(escape)
#     edit.line_end()

# image small:
#     insert("|#small")
#     key(escape)
#     edit.line_end()
close:
    key(cmd-w)

header one  [<user.text>]$:
    insert("# ")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))
    
header two  [<user.text>]$:
    insert("## ")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))

header three  [<user.text>]$:
    insert("### ")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))

header four  [<user.text>]$:
    insert("#### ")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))

header five  [<user.text>]$:
    insert("###### ")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))

header six  [<user.text>]$:
    insert("####### ")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))

split vert:
    user.obsidian_run_command("Split vertically")

bold: key(cmd-b)

# shortcuts to specific pages
kanban go:
    user.obsidian_open_note("kanban")
# go massage:
#     user.obsidian_open_note("Masa Aktualny nowy")

follow:
    key(alt-enter)
open side:
    key(alt-cmd-enter)

# TODO: this doesn't work
unbullet:
    key("alt-delete")
    
