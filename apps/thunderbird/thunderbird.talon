app: thunderbird
and not app: thunderbird_contacts
and not app: thunderbird_composer
-
# Set tags
tag(): user.tabs

# navigate tabs
go (mails | messages | inbox): user.tab_jump(1)
go (calendar | lightning): user.thunderbird_mod("shift-c")
go tasks: user.thunderbird_mod("shift-d")
# open windows
(open address [book] | address book | open contacts): user.thunderbird_mod("shift-b")
dev tools: user.thunderbird_mod("shift-i")
