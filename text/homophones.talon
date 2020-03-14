(phones | homophones) help: user.homophones_show_help()
phones <user.homophones_canonical>: user.homophones_show(homophones_canonical)
phones: user.homophones_show_selection()
force phones <user.homophones_canonical>: user.homophones_force_show(homophones_canonical)
force phones: user.homophones_force_show_selection()
hide phones: user.homophones_hide()

(pick | sell | cell) <user.homophones_selection>: 
    insert(homophones_selection)
    user.homophones_hide()

<user.homophones_formatted_selection>: 
    insert(homophones_formatted_selection)
    user.homophones_hide()