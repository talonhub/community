mode: dictation
mode: user.polish_dictation
-
^press <user.keys>$: key("{keys}")
kropka: "."
przecinek: ","
nowa linia: "\n"
^zatrzymaj$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.disable("user.polish_dictation")
    mode.enable("command")

# Everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<user.prose>: auto_insert(prose)
