mode: user.homophones
-
choose <number_small>:
    result = user.homophones_select(number_small)
    insert(result)
    user.homophones_hide()
choose <user.formatters> <number_small>:
    result = user.homophones_select(number_small)
    insert(user.formatted_text(result, formatters))
    user.homophones_hide()
