tag: user.code_macro_like
-

(macro | anno) <user.code_all_macro_like>:
    user.code_insert_macro_like(user.code_all_macro_like, "")
(macro | anno) wrap <user.code_all_macro_like>:
    user.code_insert_macro_like(user.code_all_macro_like, edit.selected_text())
