mode: user.clipboard_history
-

clip close: user.clipboard_history_toggle()

copy <number_small> [and <number_small>]*:
    user.clipboard_history_copy(number_small_list)
paste <number_small> [and <number_small>]*:
    user.clipboard_history_paste(number_small_list)
paste match style <number_small> [and <number_small>]*:
    user.clipboard_history_paste(number_small_list, 1)

clip clear [all]: user.clipboard_history_remove()

clip clear <number_small> [and <number_small>]*:
    user.clipboard_history_remove(number_small_list)

clip split <number_small> [and <number_small>]*:
    user.clipboard_history_split(number_small_list)