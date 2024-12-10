mode: command
mode: dictation
-
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    user.gdb_disable()
    user.system_command_nb("curl -X 'GET' \"http://10.0.0.151/show?letter=D\"")

^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
    user.system_command_nb("curl -X 'GET' \"http://10.0.0.151/show?letter=C\"")
