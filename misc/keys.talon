go <user.arrow_keys>: key(arrow_keys)
# I don't want to have the possibility to enter a single letter not ending with $, because it leads to to many misrecognitions
# <user.letter>: key(letter)
<user.letters>$: insert(letters) 
<user.letters> <user.special_key>$: 
    insert(letters) 
    key(special_key)  

(ship | uppercase) <user.letters> [(lowercase | sunk)]: 
    user.insert_formatted(letters, "ALL_CAPS")
<user.symbol_key>: key(symbol_key)
<user.function_key>: key(function_key)
<user.special_key>: key(special_key)
<user.modifiers> <user.unmodified_key>: key("{modifiers}-{unmodified_key}")