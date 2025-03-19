mode: sleep
speech.engine: wav2letter
-
#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
#you probably shouldn't have any other commands here
<phrase>: user.sleep_reset_deep_sleep_counter()
