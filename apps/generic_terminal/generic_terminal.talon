tag: terminal
-
# TODO: decide which tags to activate
# Or only activate for specific editors (the better way IMHO)
# TODO: file_manager-tag?

lisa: 
    user.terminal_list_directories()
lisa all: 
    user.terminal_list_all_directories()
katie [<user.text>]: user.terminal_change_directory(text or "")
katie root: user.terminal_change_directory_root()
clear screen: user.terminal_clear_screen()
run last: user.terminal_run_last()
rerun [<user.text>]: user.terminal_rerun_search(text or "")
rerun search: user.terminal_rerun_search("")
kill all: user.terminal_kill_all()