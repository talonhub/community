not mode: sleep
-
^(dictate|dictation mode) [<phrase>]$:   user.dictation_mode(phrase or "")
^(text field mode) [<phrase>]$:   user.text_field_mode(phrase or "")

^(dictate polish) [<phrase>]$:   user.polish_dictation_mode(phrase or "")
(command mode) [<phrase>]$:   user.command_mode(phrase or "")