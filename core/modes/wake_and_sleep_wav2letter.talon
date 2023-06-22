mode: all
speech.engine: wav2letter
-
^go to sleep [<phrase>]$: speech.disable()
^(wake up)+$: speech.enable()
