not mode: sleep
-
^(dictate|dictation mode)$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")
^dictate polish$:
    mode.disable("sleep")
    mode.disable("comicknd")
    mode.enable("dictation")
    mode.enable("user.polish_dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")