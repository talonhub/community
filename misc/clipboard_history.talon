mode: user.clipboard_history
-

copy <number_small> [and <number_small>]*:
    user.clipboard_history_copy(number_small_list)
paste <number_small> [and <number_small>]*:
    user.clipboard_history_paste(number_small_list)
paste match style <number_small> [and <number_small>]*:
    user.clipboard_history_paste(number_small_list, 1)

clipboard [history] close: user.clipboard_history_toggle()

clipboard [history] clear [all]: user.clipboard_history_remove()

clipboard [history] clear <number_small> [and <number_small>]*:
    user.clipboard_history_remove(number_small_list)

clipboard [history] split <number_small> [and <number_small>]*:
    user.clipboard_history_split(number_small_list)
