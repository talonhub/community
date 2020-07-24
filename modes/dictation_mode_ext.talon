mode: dictation
-
capitalize <user.text>:
    insert(user.formatted_text(text, "CAPITALIZE_FIRST_WORD"))
<user.text>:
    insert(user.text)
    insert(" ")

delete: key(backspace)
