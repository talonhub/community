#defines the commands that sleep/wake Talon
mode: all
-
^welcome back$: user.welcome_back()
^sleep all$: user.sleep_all()
^go to sleep$: speech.disable()
^wake up$: speech.enable()


