tag: user.code_comment_line
-

comment: user.code_comment_line_prefix()
comment line:
    edit.line_start()
    user.code_comment_line_prefix()
#adds comment to the start of the line
comment line <user.text> {user.phrase_ender}:
    edit.line_start()
    user.code_comment_line_prefix()
    insert(user.text)
    insert(" ")
comment <user.text> {user.phrase_ender}:
    user.code_comment_line_prefix()
    insert(user.text)
comment <user.text>$:
    user.code_comment_line_prefix()
    insert(user.text)
(line | inline) comment <user.text> {user.phrase_ender}:
    edit.line_end()
    user.code_comment_line_prefix()
    insert(user.text)
(line | inline) comment <user.text>$:
    edit.line_end()
    user.code_comment_line_prefix()
    insert(user.text)
