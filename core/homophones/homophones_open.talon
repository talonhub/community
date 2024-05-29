tag: user.homophones_open
-
tag(): user.choose_selector

choose <number_small>:
    result = user.choose(number_small)
choose <user.formatters> <number_small>:
    result = user.homophones_select(number_small)
    insert(user.formatted_text(result, formatters))
    user.homophones_hide()
