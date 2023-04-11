mode: all
-
^deep sleep$:    
    speech.disable()
    mode.enable("user.deep_sleep")

^talon please wake up$:
    speech.enable()
    mode.disable("user.deep_sleep")