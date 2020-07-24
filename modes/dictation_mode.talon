mode: dictation
-
capitalize <user.text>:
    insert(user.formatted_text(text, "CAPITALIZE_FIRST_WORD"))
<user.text>:
    insert(user.text)
    insert(" ")
enter: key(enter)
period: key(backspace . space)
comma: key(backspace , space)
question [mark]: key(backspace ? space)
delete: key(backspace)
(bang | exclamation [mark]): key(backspace ! space)
