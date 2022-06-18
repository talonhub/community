#defines modes specific to Dragon.
speech.engine: dragon
mode: all
-
# wakes Dragon on Mac, deactivates talon speech commands
dragon mode: user.dragon_mode()
#sleep dragon on Mac, activates talon speech commands
talon mode: user.talon_mode()
