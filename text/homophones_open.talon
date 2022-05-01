mode: user.homophones
-
<number_small>:
    result = user.homophones_select(number_small)
    insert(result)
    user.homophones_hide()
choose <user.formatters> <number_small>: #TODO. what is the user.formatter? i changed the above to remove the choose, but don't know whwat this part is for so dont want to mess it up. TODO.
    result = user.homophones_select(number_small)
    insert(user.formatted_text(result, formatters))
    user.homophones_hide()
