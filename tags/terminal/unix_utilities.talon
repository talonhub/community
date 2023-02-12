tag: user.unix_utilities
-

# curated list of commands with defined arguments:
core {user.unix_utility} [<user.unix_arguments>] [over]:
    args = unix_arguments or ""
    "{unix_utility}{args}"

# standalone arguments (predefined arguments preferred)
param [<user.unix_free_form_argument>]:
    insert(" --{unix_free_form_argument or ''}")
param (single|sing) [<user.unix_free_form_argument>]:
    insert(" -{unix_free_form_argument or ''}")
flag [<user.letter>]: " -{letter or ''}"
# flag shift/ship/uppercase <letter> produces the uppercase variant
dubdash: " -- "
