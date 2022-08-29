tag: terminal
-
# tags should be activated for each specific terminal in the respective talon file

lisa: 
    user.terminal_list_directories()
lisa all: 
    user.terminal_list_all_directories()
#katie [<user.text>]: user.terminal_change_directory(text or "")
#katie root: user.terminal_change_directory_root()
cathy [<user.text>]: user.terminal_change_directory(text or "")
cathy root: user.terminal_change_directory_root()
victor [<user.text>]: 
    insert("vim ")
    insert(text or "")
    sleep(50ms)
    key(tab)
victor safe: insert("vim -R ")
gary [<user.text>]:
    insert('grep -nr --include="*.R" ""')
    key(left)
    key(left)
    key(left)
    insert(text or "")
greta [<user.text>]: 
    insert('grep -nr "" .')
    key(left)
    key(left)
    key(left)  
    insert(text or "")
fiona [<user.text>]:
    insert('find . -type f -name ""')
    key(left)
    insert(text or "")
mickie [<user.text>]:
    insert('mkdir ')
    insert(text or "")

copy output:
    key(cmd-shift-a)
    edit.copy()


clear screen: user.terminal_clear_screen()
run last: user.terminal_run_last()
rerun [<user.text>]: user.terminal_rerun_search(text or "")
rerun search: user.terminal_rerun_search("")
kill all: user.terminal_kill_all()

go talon: user.terminal_change_directory("~/.talon/user/knausj_talon/")
save and exit:
    key(escape)
    insert(":x")
    key(enter)

copy paste:
    edit.copy()
    sleep(50ms)
    edit.paste()
