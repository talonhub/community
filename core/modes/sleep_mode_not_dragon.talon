mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
not tag: user.deep_sleep
-

# We define this *only* if the speech engine isn't Dragon, because if you're using Dragon,
# "wake up" is used to specifically control Dragon, and not affect Talon.
#
# It's a useful and well known command, though, so if you're using any other speech
# engine, this controls Talon.

^(wake up)+$: speech.enable()
