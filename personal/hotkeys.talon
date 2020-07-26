key(ctrl-pagedown): speech.disable()
key(ctrl-pageup): speech.enable()
key(ctrl-end):
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
key(ctrl-home):
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
key(ctrl-f20): user.history_enable()
key(ctrl-del): user.history_disable()