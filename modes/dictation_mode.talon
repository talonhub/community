mode: dictation
-
^press <user.keys>$: key("{keys}")

# Everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<user.text>: auto_insert(text)
{user.punctuation}: auto_insert(punctuation)
new line: auto_insert("new-line")
new paragraph: auto_insert("new-paragraph")
cap <user.word>:
    result = user.formatted_text(word, "CAPITALIZE_FIRST_WORD")
    auto_insert(result)
    
# Navigation
go up <number_small> (line|lines):
    edit.up()
    repeat(number_small - 1)
go down <number_small> (line|lines):
    edit.down()
    repeat(number_small - 1)
go left <number_small> (word|words):
    edit.word_left()
    repeat(number_small - 1)
go right <number_small> (word|words):
    edit.word_right()
    repeat(number_small - 1)
go line start: edit.line_start()
go line end: edit.line_end()

# Selection
select left <number_small> (word|words):
    edit.extend_word_left()
    repeat(number_small - 1)
select right <number_small> (word|words):
    edit.extend_word_right()
    repeat(number_small - 1)
select left <number_small> (character|characters):
    edit.extend_left()
    repeat(number_small - 1)
select right <number_small> (character|characters):
    edit.extend_right()
    repeat(number_small - 1)
clear left <number_small> (word|words):
    edit.extend_word_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (word|words):
    edit.extend_word_right()
    repeat(number_small - 1)
    edit.delete()
clear left <number_small> (character|characters):
    edit.extend_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (character|characters):
    edit.extend_right()
    repeat(number_small - 1)
    edit.delete()

# Formatting
formatted <user.format_text>:
    user.auto_format_pause()
    auto_insert(format_text)
    user.auto_format_resume()
^format selection <user.formatters>$:
    user.formatters_reformat_selection(formatters)

# Corrections
scratch that: user.clear_last_utterance()
scratch selection: edit.delete()
select that: user.select_last_utterance()
spell that <user.letters>: auto_insert(letters)
spell that <user.formatters> <user.letters>:
    result = user.formatted_text(letters, formatters)
    user.auto_format_pause()
    auto_insert(result)
    user.auto_format_resume()

# Escape, type things that would otherwise be commands
^escape <user.text>$:
    auto_insert(user.text)
