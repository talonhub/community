-
dictate [<phrase>]$:   user.dictation_mode(phrase or "")
# ^(text field mode) [<phrase>]$:   user.text_field_mode(phrase or "")
^polish$: 
    mode.disable("command")
    mode.enable("dictation")
    mode.enable("user.polish")
webspeech english [<phrase>]$:   user.webspeech_english_dictation_mode(phrase or "")
command mode [<phrase>]$:   user.command_mode(phrase or "")
