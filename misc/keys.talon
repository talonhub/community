go <user.arrows>: key(arrows)
#disabled due to https://github.com/talonvoice/beta/issues/90
#<user.number>: key(number)
<user.letter>: key(letter)
(ship | uppercase) <user.letters> [(lowercase | sunk)]: 
    user.keys_uppercase_letters(letters)
<user.symbol>: key(symbol)
<user.function>: key(function)
<user.special>: key(special)
<user.key>: key(key)
