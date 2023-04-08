tag: user.code_comment_line
-
note: user.code_comment_line_prefix()
note:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_start()
    user.code_comment_line_prefix()
#adds comment to the start of the line
note <user.text> over:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_start()
    user.code_comment_line_prefix()
    insert(user.text)
    insert(" ")
note <user.text> over:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    user.code_comment_line_prefix()
    insert(user.text)
note <user.text>$:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    user.code_comment_line_prefix()
    insert(user.text)
(line | inline) note <user.text> over:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_end()
    user.code_comment_line_prefix()
    insert(user.text)
(line | inline) note <user.text>$:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_end()
    user.code_comment_line_prefix()
    insert(user.text)
