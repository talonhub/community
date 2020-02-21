(phones | homophones) help: user.knausj_talon.actions.homophones.show_homophones_help()
phones <user.knausj_talon.actions.homophones.canonical>: user.knausj_talon.actions.homophones.show_homophones(user.knausj_talon.actions.homophones.canonical)
phones: user.knausj_talon.actions.homophones.show_homophones_selection()
force phones <user.knausj_talon.actions.homophones.canonical>: user.knausj_talon.actions.homophones.force_show_homophones(user.knausj_talon.actions.homophones.canonical)
force phones: user.knausj_talon.actions.homophones.force_show_homophones_selection()
hide phones: user.knausj_talon.actions.homophones.hide_homophones()

(pick | sell | cell) <user.knausj_talon.actions.homophones.selection>: 
    insert(user.knausj_talon.actions.homophones.selection)
    user.knausj_talon.actions.homophones.hide_homophones()

(pick | sell | cell) <user.knausj_talon.actions.formatters.formatters> <user.knausj_talon.actions.homophones.selection>: 
    user.knausj_talon.actions.formatters.format_word(user.knausj_talon.actions.homophones.selection, user.knausj_talon.actions.formatters.formatters)
    user.knausj_talon.actions.homophones.hide_homophones()
