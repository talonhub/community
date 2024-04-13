app: thunderbird_inbox
-
# navigate
(mail | message) open: key(enter)
(mail | message) (up | last): key(b)
(mail | message) (down | next): key(f)
unread [mail | message] (up | last): key(p)
unread [mail | message] (down | next): key(n)
go home: key(alt-home)
toggle (mail | message) [pane]: key(f8)
# mark
(mail | message) (favorite | unfavorite): key(s)
(mail | message) (read | unread): key(m)
(mail | message) (watch | unwatch): key(w)
(mail | message) (ignore | unignore): key(k)
(mail | message) suspend: key(c)
(mail | message) spam: key(j)
# send
(mail | message) new: user.thunderbird_mod("n")
(mail | message) edit: user.thunderbird_mod("e")
(mail | message) reply sender: user.thunderbird_mod("r")
(mail | message) reply all: user.thunderbird_mod("shift-r")
(mail | message) reply list: user.thunderbird_mod("shift-l")
(mail | message) forward: user.thunderbird_mod("l")
# organize
(mail | message) delete: key(delete)
(mail | message) archive: key(a)
(mail | message) save: user.thunderbird_mod("s")
(mail | message) print: user.thunderbird_mod("p")
