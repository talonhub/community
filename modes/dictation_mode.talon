mode: dictation
-
#everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<user.text>: auto_insert(text)
enter: auto_insert("new-line")
period: auto_insert(".")
(comma | kama): 
    auto_insert(",")
question mark: auto_insert("?")
(bang | exclamation [mark]): auto_insert("!")
dash: auto_insert("-")
colon: auto_insert(":")
space: user.dictate(" ")
(semi colon | semicolon): auto_insert(";")
cap <user.text>: 
    result = user.formatted_text(user.text, "CAPITALIZE_FIRST_WORD")
    auto_insert(result)
#navigation
go up <number_small> lines:
    edit.up()
    repeat(number_small - 1)
go down <number_small> lines:
    edit.down()
    repeat(number_small - 1)
go left <number_small> words: 
    edit.word_left()
    repeat(number_small - 1)
go right <number_small> words: 
    edit.word_right()
    repeat(number_small - 1)
go line start: edit.line_start()
go line end: edit.line_end()
#selection
select left <number_small> words:
    edit.extend_word_left()
    repeat(number_small - 1)
select right <number_small> words:
    edit.extend_word_right()
    repeat(number_small - 1)
select left <number_small> characters:
    edit.extend_left()
    repeat(number_small - 1)
select right <number_small> characters:
    edit.extend_right()
    repeat(number_small - 1)
clear left <number_small> words:
    edit.extend_word_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> words:
    edit.extend_word_right()
    repeat(number_small - 1)
    edit.delete()
clear left <number_small> characters:
    edit.extend_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> characters:
    edit.extend_right()
    repeat(number_small - 1)
    edit.delete()
#formatting 
formatted <user.format_text>:
    user.auto_format_pause()
    auto_insert(format_text)
    user.auto_format_resume()
^format selection <user.formatters>$:
    user.formatters_reformat_selection(formatters)
#corrections
scratch that: user.clear_last_utterance()
scratch selection: edit.delete()
select that: user.select_last_utterance()
spell that <user.formatters> <user.letters>:
    result = dictate.join_words(user.letters, "")
    result = user.formatted_text(result, formatters)
    user.auto_format_pause()
    auto_insert(result)
    user.auto_format_resume()
spell that <user.letters>:
    result = dictate.join_words(user.letters, "")
    auto_insert(result)
#escape, type things that would otherwise be commands
^escape <user.text>$:
    auto_insert(user.text)
