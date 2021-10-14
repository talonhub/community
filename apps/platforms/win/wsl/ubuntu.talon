app: ubuntu
app: windows_terminal
and win.title: /Ubuntu/
-
tag(): terminal
tag(): user.file_manager
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.kubectl

^go <user.letter>$: user.file_manager_open_volume("/mnt/{letter}")
