(phones | homophones) help: user.actions.homophones.show_homophones_help()
phones <user.actions.homophones.canonical>: user.actions.homophones.show_homophones(user.actions.homophones.canonical)
phones: user.actions.homophones.show_homophones_selection()
force phones <user.actions.homophones.canonical>: user.actions.homophones.force_show_homophones(user.actions.homophones.canonical)
force phones: user.actions.homophones.force_show_homophones_selection()
hide phones: user.actions.homophones.hide_homophones()

(pick | sell | cell) <user.actions.homophones.selection>: 
    insert(user.actions.homophones.selection)
    user.actions.homophones.hide_homophones()

(pick | sell | cell) <user.actions.formatters.formatters> <user.actions.homophones.selection>: 
    user.actions.formatters.format_word(user.actions.homophones.selection, user.actions.formatters.formatters)
    user.actions.homophones.hide_homophones()
