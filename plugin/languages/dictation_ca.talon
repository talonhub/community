mode: dictation
language: ca
-
#[<user.text>] (al anglès | a l'anglès):
^anglès:
    mode.disable("dictation")
    mode.disable("user.catalan")
    mode.enable("command")

eliminar paraula:
    edit.delete_word()

eliminar caràcter:
    edit.delete_left()

eliminar línia:
    edit.delete_line()

(intro | enter):
    key("enter")

<phrase>: insert("{phrase} ")