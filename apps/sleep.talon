not mode: sleep
-
key(cmd-alt-n):
    user.history_disable()
    speech.disable()
    mode.disable("noise")
    mode.disable("dictation")
    mode.disable("command")
    app.notify("back to sleep")

key(cmd-ctrl-b):
    user.history_disable()
    speech.disable()
    mode.disable("noise")
    mode.disable("dictation")
    mode.disable("command")
    app.notify("back to sleep")