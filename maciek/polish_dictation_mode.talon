mode: user.polish
-
^press <user.keys>$: key("{keys}")
(kropka|kropkę): "."
przecinek: ","
(nowa linia|enter): "\n" 
dwukropek: ":"
znak zapytania: "?"
myślnik: "-"
# (skończ|kończ|kończy) [<phrase>]$:   user.command_mode(phrase or "")
(post|Post) [<phrase>]$:   user.command_mode(phrase or "")
masował m: auto_insert("masowałem")

# Everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<user.prose>: auto_insert(prose)
