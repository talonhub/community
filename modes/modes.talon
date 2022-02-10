not mode: sleep
-
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")
    # user.engine_sleep()
^command mode$:
    # user.engine_sleep()
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
    