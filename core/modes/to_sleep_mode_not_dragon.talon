mode: command
mode: dictation
not speech.engine: dragon
-
# We define this *only* if the speech engine isn't Dragon, because if you're using Dragon,
# "go to sleep" is used to specifically control Dragon, and not affect Talon.
#
# If you're using any other speech engine, this controls Talon.
^go to sleep [<phrase>]$: speech.disable()
