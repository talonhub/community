tag: terminal
tag: user.generic_unix_shell
os: mac
os: linux
-
# Generic Shell Commands. (General convension is to use the command name in "man" when possible)

^change (directory|dir)$: "cd "
^home (directory|dir)$: "~/"
^copy$: "cp "
^make dir$: "mkdir "
^cancel$: key(ctrl-c)
^(move|rename) command: "mv "
^list directory$: "ls "
^list current directory$: user.terminal_list_directories()
^grep$: "grep "
^edit$: "vi " # Can be replaced with your favorite editor
^less$: "less "
^remove$: "rm "
^teemux$: "tmux "
^netstat$: "netstat "
^which$: "which "
^touch$: "touch "
^real path$: "realpath "
^echo$: "echo "
^working directory [name]$: "pwd\n"
