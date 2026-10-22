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

#################
# Dictation mode uses some commands from command mode
# These are indicated with `# from <original_file>`

# from core/keys/keys.talon
^press <user.modifiers>$: key(modifiers)
^press <user.keys>$: key(keys)

# from core/edit/edit.talon
<user.edit_action> <user.edit_modifier>: user.edit_command(edit_action, edit_modifier)
# Navigation
go <user.navigation_step>+: user.perform_navigation_steps(navigation_step_list)
go line start: edit.line_start()
go line end: edit.line_end()

# Corrections
# from core/text/text.talon
nope that | scratch that: user.clear_last_phrase()
select that: user.select_last_phrase()
