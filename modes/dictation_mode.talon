mode: dictation
-
#everything here should call user.dictate to preserve the state to correctly auto-capitalize.
<user.text>: user.dictate(text)
enter: user.dictate("new-line")
period: user.dictate(".")
comma: user.dictate(",")
question [mark]: user.dictate("?")
(bang | exclamation [mark]): user.dictate("!")
dash: user.dictate("-")
colon: user.dictate(":")
semi colon: user.dictate(";")
cap <user.text>: 
    result = user.formatted_text(user.text, "CAPITALIZE_FIRST_WORD")
    user.dictate(result)  
