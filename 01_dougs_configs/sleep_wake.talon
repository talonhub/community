#defines the commands that sleep/wake Talon
mode: all
-

^drowse [<phrase>]$: speech.disable()
^talon wake$: speech.enable()

