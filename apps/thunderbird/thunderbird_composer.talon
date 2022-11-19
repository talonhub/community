app: thunderbird_composer
-
# mail
(draft | mail | message) save: user.thunderbird_mod("s")
(draft | mail | message) print: user.thunderbird_mod("p")
(draft | mail | message) send: user.thunderbird_mod("enter")
# layout
toggle contacts: key(f9)
# navigation
go (inbox | thunderbird | main): user.thunderbird_mod("1")
# edit
cite paste: user.thunderbird_mod("shift-o")
(unformatted | raw) paste: user.thunderbird_mod("shift-v")
link new: user.thunderbird_mod("k")
link delete: user.thunderbird_mod("shift-k")
