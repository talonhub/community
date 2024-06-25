# This makes it easier to chain commands by letting you hint about command boundaries.
# For example, with Cursorless, the phrase "post line air" is ambiguous as to whether you meant a single command ("post line air", i.e. "move the cursor to the end of the line containing the 'a' hat"), or two separate commands ("post line" to move the cursor to the end of the current line, followed by "air" to insert the letter "a").
# If you know you want the latter, this allows you to say "post line then air" to force that interpretation.
then: skip()
