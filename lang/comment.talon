tag: user.code_comment
-
comment: user.code_comment()
comment line: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_start()
    user.code_comment()
#adds comment to the start of the line
comment line <user.text> over: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_start()
    user.code_comment()
	insert(user.text)
    insert(" ")
comment line <user.text> over: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_start()
    user.code_comment()
    insert(user.text)
    insert(" ")
comment <user.text> over: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	user.code_comment()
    insert(user.text)
^comment <user.text>$: 
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    user.code_comment()
    insert(user.text)
(line | inline) comment <user.text> over:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_end()
   	user.code_comment()
    insert(user.text)
^(line | inline) comment <user.text>$:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_end()
   	user.code_comment()
    insert(user.text)
