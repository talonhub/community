mode: dictation
-
^press <user.modifiers>$: key(modifiers)
^press <user.keys>$: key(keys)

# Everything here should call `user.dictation_insert()` instead of `insert()`, to correctly auto-capitalize/auto-space.
<user.raw_prose>: user.dictation_insert(raw_prose)
cap: user.dictation_format_cap()
# Hyphenated variants are for Dragon.
(no cap | no-caps): user.dictation_format_no_cap()
(no space | no-space): user.dictation_format_no_space()
^cap that$: user.dictation_reformat_cap()
^(no cap | no-caps) that$: user.dictation_reformat_no_cap()
^(no space | no-space) that$: user.dictation_reformat_no_space()

# Navigation
go up <number_small> (line | lines):
    edit.up()
    repeat(number_small - 1)
go down <number_small> (line | lines):
    edit.down()
    repeat(number_small - 1)
go left <number_small> (word | words):
    edit.word_left()
    repeat(number_small - 1)
go right <number_small> (word | words):
    edit.word_right()
    repeat(number_small - 1)
go line start: edit.line_start()
go line end: edit.line_end()

# Selection
select left <number_small> (word | words):
    edit.extend_word_left()
    repeat(number_small - 1)
select right <number_small> (word | words):
    edit.extend_word_right()
    repeat(number_small - 1)
select left <number_small> (character | characters):
    edit.extend_left()
    repeat(number_small - 1)
select right <number_small> (character | characters):
    edit.extend_right()
    repeat(number_small - 1)
clear left <number_small> (word | words):
    edit.extend_word_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (word | words):
    edit.extend_word_right()
    repeat(number_small - 1)
    edit.delete()
clear left <number_small> (character | characters):
    edit.extend_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (character | characters):
    edit.extend_right()
    repeat(number_small - 1)
    edit.delete()

# Formatting
formatted <user.format_text>: user.dictation_insert_raw(format_text)
^format selection <user.formatters>$: user.formatters_reformat_selection(formatters)

# Corrections
nope that | scratch that: user.clear_last_phrase()
(nope | scratch) selection: edit.delete()
select that: user.select_last_phrase()
spell that <user.letters>: user.dictation_insert(letters)
spell that <user.formatters> <user.letters>:
    result = user.formatted_text(letters, formatters)
    user.dictation_insert_raw(result)

# Escape, type things that would otherwise be commands
^escape <user.text>$: user.dictation_insert(user.text)
