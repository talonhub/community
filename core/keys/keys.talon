not tag: user.homerow_search
not tag: user.fluent_search_screen_search
-
<user.letter>: key(letter)
(ship | uppercase) <user.letters> [(lowercase | sunk)]:
    user.insert_formatted(letters, "ALL_CAPS")
<user.symbol_key>: key(symbol_key)
<user.function_key>: key(function_key)
<user.special_key>: key(special_key)
<user.modifiers> <user.unmodified_key>: key("{modifiers}-{unmodified_key}")
# for key combos consisting only of modifiers, eg. `press super`.
press <user.modifiers>: key(modifiers)
# for consistency with dictation mode and explicit arrow keys if you need them.
press <user.keys>: key(keys)
shift up [<number_small>]:
    numb  = number_small or 1
    key(shift-up)
    repeat(numb - 1)
shift down [<number_small>]:
    numb  = number_small or 1
    key(shift-down)
    repeat(numb - 1)
shift tab [<number_small>]:
    numb  = number_small or 1
    key(shift-tab)
    repeat(numb - 1)
tab <number_small>:
    numb  = number_small or 1
    key(tab)
    repeat(numb - 1)
    