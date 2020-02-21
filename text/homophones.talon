(phones | homophones) help: user.knausj_talon.code.homophones.show_homophones_help()
phones <user.knausj_talon.code.homophones.canonical>: user.knausj_talon.code.homophones.show_homophones(user.knausj_talon.code.homophones.canonical)
phones: user.knausj_talon.code.homophones.show_homophones_selection()
force phones <user.knausj_talon.code.homophones.canonical>: user.knausj_talon.code.homophones.force_show_homophones(user.knausj_talon.code.homophones.canonical)
force phones: user.knausj_talon.code.homophones.force_show_homophones_selection()
hide phones: user.knausj_talon.code.homophones.hide_homophones()

(pick | sell | cell) <user.knausj_talon.code.homophones.selection>: 
    insert(user.knausj_talon.code.homophones.selection)
    user.knausj_talon.code.homophones.hide_homophones()

(pick | sell | cell) <user.knausj_talon.code.formatters.formatters> <user.knausj_talon.code.homophones.selection>: 
    user.knausj_talon.code.formatters.format_word(user.knausj_talon.code.homophones.selection, user.knausj_talon.code.formatters.formatters)
    user.knausj_talon.code.homophones.hide_homophones()
