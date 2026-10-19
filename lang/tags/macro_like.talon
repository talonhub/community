tag: user.code_macro_like
-

(macro | anno) {user.code_basic_macro_likes}:
    user.code_insert_basic_macro_like(code_basic_macro_likes)

(macro | anno) {user.code_function_macro_likes}:
    user.code_insert_function_macro_like(code_function_macro_likes, "")
(macro | anno) wrap {user.code_function_macro_likes}:
    user.code_insert_function_macro_like(code_function_macro_likes, edit.selected_text())

(macro | anno) {user.code_array_macro_likes}:
    user.code_insert_macro_array_like(code_array_macro_likes, "")
(macro | anno) wrap {user.code_array_macro_likes}:
    user.code_insert_macro_array_like(code_array_macro_likes, edit.selected_text())

(macro | anno) {user.code_block_macro_likes}:
    user.code_insert_macro_block_like(code_block_macro_likes, "")
(macro | anno) wrap {user.code_block_macro_likes}:
    user.code_insert_macro_block_like(code_block_macro_likes, edit.selected_text())
