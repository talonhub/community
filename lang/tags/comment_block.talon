tag: user.code_comment_block
-
block comment: user.code_comment_block()
block comment line:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_start()
    user.code_comment_block_prefix()
    key(space)
	edit.line_end()
    key(space)
    user.code_comment_block_suffix()
#adds comment to the start of the line
block comment line <user.text> over:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    edit.line_start()
    user.code_comment_block()
	insert(user.text)
block comment <user.text> over:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	user.code_comment_block()
    insert(user.text)
block comment <user.text>$:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
    user.code_comment_block()
    insert(user.text)
(line | inline) block comment <user.text> over:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_end()
   	user.code_comment_block_prefix()
    key(space)
    insert(user.text)
    key(space)
   	user.code_comment_block_suffix()
(line | inline) block comment <user.text>$:
    #todo: this should probably be a single function once
    #.talon supports implementing actions with parameters?
	edit.line_end()
   	user.code_comment_block_prefix()
    key(space)
    insert(user.text)
    key(space)
   	user.code_comment_block_suffix()
open block comment:
    user.code_comment_block_prefix()
close block comment:
    user.code_comment_block_suffix()
