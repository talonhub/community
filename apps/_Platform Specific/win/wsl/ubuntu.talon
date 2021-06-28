app: ubuntu
app: windows_terminal
and win.title: /Ubuntu/
-
tag(): user.file_manager
tag(): user.generic_terminal
tag(): user.git
tag(): user.kubectl
tag(): terminal
^go <user.letter>$: user.file_manager_open_volume("/mnt/{letter}")
