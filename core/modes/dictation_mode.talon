mode: dictation
-

# Everything here should call `user.dictation_insert()` instead of `insert()`, to correctly auto-capitalize/auto-space.
<user.raw_prose>: user.dictation_insert(raw_prose)
cap: user.dictation_format_cap()
# Hyphenated variants are for Dragon.
no cap | no-caps: user.dictation_format_no_cap()
no space | no-space: user.dictation_format_no_space()
^cap that$: user.dictation_reformat_cap()
^(no cap | no-caps) that$: user.dictation_reformat_no_cap()
^(no space | no-space) that$: user.dictation_reformat_no_space()

spell that <user.letters>: user.dictation_insert(letters)
spell that <user.formatters> <user.letters>:
    result = user.formatted_text(letters, formatters)
    user.dictation_insert_raw(result)

# Formatting
formatted <user.format_text>: user.dictation_insert_raw(format_text)
^format selection <user.formatters>$: user.formatters_reformat_selection(formatters)

# Escape, type things that would otherwise be commands
^escape <user.text>$: user.dictation_insert(user.text)

(nope | scratch) selection: edit.delete()

############################
# Copied from command mode
^press <user.modifiers>$: key(modifiers)
^press <user.keys>$: key(keys)
<user.edit_action> <usertedit_modifier>: user.edit_command(edit_action, edit_modifier)
go <user.navigation_step>+: user.perform_navigation_steps(navigation_step_list)
go line start: edit.line_start()
go line end: edit.line_end()
# Corrections
nope that | scratch that: user.clear_last_phrase()
select that: user.select_last_phrase()

####################
# DEPRECATED BEGIN #
# Navigation
go up <number_small> (line | lines):
    user.deprecate_command("2026-10-23", "go up <number_small> (line | lines)", "go <number_small> up")
    edit.up()
    repeat(number_small - 1)
go down <number_small> (line | lines):
    user.deprecate_command("2026-10-23", "go down <number_small> (line | lines)", "go <number_small> down")
    edit.down()
    repeat(number_small - 1)
go left <number_small> (word | words):
    user.deprecate_command("2026-10-23", "go left <number_small> (word | words)", "go <number_small> word left")
    edit.word_left()
    repeat(number_small - 1)
go right <number_small> (word | words):
    user.deprecate_command("2026-10-23", "go right <number_small> (line | lines)", "go <number_small> word right")
    edit.word_right()
    repeat(number_small - 1)
go left <number_small> (character | characters):
    user.deprecate_command("2026-10-23", "go left <number_small> (character | characters)", "go <number_small> left")
    edit.left()
    repeat(number_small - 1)
go right <number_small> (character | characters):
    user.deprecate_command("2026-10-23", "go right <number_small> (character | characters)", "go <number_small> right")
    edit.right()
    repeat(number_small - 1)
select left <number_small> (word | words):
    user.deprecate_command("2026-10-23", "select left <number_small> (word | words)", "select <number_small> word left")
    edit.extend_word_left()
    repeat(number_small - 1)
select right <number_small> (word | words):
    user.deprecate_command("2026-10-23", "select right <number_small> (line | lines)", "select <number_small> word right")
    edit.extend_word_right()
    repeat(number_small - 1)
select left <number_small> (character | characters):
    user.deprecate_command("2026-10-23", "select left <number_small> (character | characters)", "select <number_small> left")
    edit.extend_left()
    repeat(number_small - 1)
select right <number_small> (character | characters):
    user.deprecate_command("2026-10-23", "select right <number_small> (character | characters)", "select <number_small> right")
    edit.extend_right()
    repeat(number_small - 1)
clear left <number_small> (word | words):
    user.deprecate_command("2026-10-23", "clear left <number_small> (word | words)", "clear <number_small> word left")
    edit.extend_word_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (word | words):
    user.deprecate_command("2026-10-23", "clear right <number_small> (line | lines)", "clear <number_small> word right")
    edit.extend_word_right()
    repeat(number_small - 1)
    edit.delete()
clear left <number_small> (character | characters):
    user.deprecate_command("2026-10-23", "clear left <number_small> (character | characters)", "clear <number_small> left")
    edit.extend_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (character | characters):
    user.deprecate_command("2026-10-23", "clear right <number_small> (character | characters)", "clear <number_small> right")
    edit.extend_right()
    repeat(number_small - 1)
    edit.delete()
# DEPRECATED END #
##################
