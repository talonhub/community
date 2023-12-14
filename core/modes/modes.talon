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

# Normally, the wake commands are only bound in sleep mode.
# However, sometimes people accidentally use them if Talon is already active, and if they're not bound, they'll likely be recognized as a different command (like "page up").
# So we bind them here, and show a notification instead to guide the user.
^(wake up | talon wake)+$: app.notify("talon is already awake")
