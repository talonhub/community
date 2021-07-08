mode: dictation
mode: user.polish_dictation
-
^press <user.keys>$: key("{keys}")
kropka: "."
przecinek: ","
nowa linia: "\n"
(koniec) [<phrase>]$:   user.command_mode(phrase or "")

# Everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<user.prose>: auto_insert(prose)
