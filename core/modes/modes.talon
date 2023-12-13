not mode: sleep
-
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    user.gdb_disable()
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")

# Without this command, talon will interpret "wake up" as another command ("page up", for example)
# This happens because the _real_ "wake up" is only active in mode:sleep
# These commands catch the redundant "wake up" command and notify the user that talon is already awake
^(wake up|talon wake)+$: app.notify("talon is already awake")
