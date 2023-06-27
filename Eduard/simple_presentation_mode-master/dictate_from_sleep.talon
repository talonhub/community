mode: sleep

-

^dictate <phrase>: 
    mode.enable('dictation')
    mode.disable('sleep')
    user.try_to_mimic("{phrase}")
    mode.disable('dictation')
    mode.enable('sleep')    




