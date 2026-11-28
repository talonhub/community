tag: user.homophones_open
-

choose <user.formatters> <number_small>:
    result = user.homophones_select(number_small)
    user.homophones_close_with_insert(user.formatted_text(result, formatters))
