mode: user.whisper
-
key(cmd-shift-1):
    res = user.whisper_stop_dictation()
    print("got")
    print(res)
    insert(res)
    user.command_mode()
