mode: dictation
language: pl
-
^press <user.keys>$: key("{keys}")
(kropka|kropkę): "."
przecinek: ","
(nowa linia|enter): "\n" 
dwukropek: ":"
znak zapytania: "?"
myślnik: "-"
# (skończ|kończ|kończy) [<phrase>]$:   user.command_mode(phrase or "")

(post|Post)$:
    mode.disable("dictation")
    mode.disable("user.polish")
    mode.enable("command")


# (post|Post) [<phrase>]$w,h
h  
#      user.command_mode(phrase or "")
masował m: auto_insert("masowałem")

# Everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<phrase>: auto_insert("{phrase}")
 

