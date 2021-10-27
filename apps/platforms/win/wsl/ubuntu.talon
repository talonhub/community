app: ubuntu
app: windows_terminal
win.title: /^WSL:/
-
tag(): terminal
tag(): user.file_manager
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.kubectl
tag(): user.wsl

^go <user.letter>$: user.file_manager_open_volume("/mnt/{letter}")
