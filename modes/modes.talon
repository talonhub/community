not mode: sleep
-
(dictate|sick) [<phrase>]$:   user.dictation_mode(phrase or "")
^(text field mode) [<phrase>]$:   user.text_field_mode(phrase or "")

polish [<phrase>]$:   user.webspeech_polish_dictation_mode(phrase or "")
webspeech english [<phrase>]$:   user.webspeech_english_dictation_mode(phrase or "")
command mode [<phrase>]$:   user.command_mode(phrase or "")
