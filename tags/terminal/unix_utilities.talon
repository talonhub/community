tag: user.unix_utilities
-

# curated list/ bag of commands approach:
core {user.unix_utility} [<user.unix_arguments>]:
    args = unix_arguments or ""
    "{unix_utility}{args}"

option <user.unix_arguments>: "{unix_arguments}"

# generic formatting (from diskordanz/2d6)
param [<user.text>]: user.insert_formatted(" --{text or ''}", "DASH_SEPARATED")
flag [<user.letter>]: " -{letter or ''}"
# flag shift/ship/uppercase <letter> produces the uppercase variant
