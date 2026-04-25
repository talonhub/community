tag: user.code_comment_block
-

block comment: user.code_comment_block()
block comment line: user.code_comment_block_line()
#adds comment to the start of the line
block comment line <user.text> over:
    edit.line_start()
    user.code_block_comment_inline(text)
block comment <user.text> over: user.code_comment_block(text)
block comment <user.text>$: user.code_comment_block(text)
(line | inline) block comment <user.text> over:
    edit.line_end()
    user.code_block_comment_inline(text)
(line | inline) block comment <user.text>$:
    edit.line_end()
    user.code_block_comment_inline(text)
open block comment: user.code_comment_block_prefix()
close block comment: user.code_comment_block_suffix()
