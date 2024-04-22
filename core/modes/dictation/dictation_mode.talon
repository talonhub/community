mode: dictation
-
settings():
    user.context_sensitive_dictation = true 
    
# ^press <user.modifiers>$: key(modifiers)
# ^press <user.keys>$: key(keys)

# Everything here should call `auto_insert()` (instead of `insert()`), to preserve the state to correctly auto-capitalize/auto-space.
# (Talonscript string literals implicitly call `auto_insert`, so there's no need to wrap those)
<user.raw_prose>: user.dictation_insert(raw_prose)
{user.punctuation}: auto_insert(punctuation)

# Escape, type things that would otherwise be commands
^escape <user.text>$: user.dictation_insert(user.text)

# Corrections
nope that | scratch that: user.clear_last_phrase()
(nope | scratch) selection: edit.delete()
select that: user.select_last_phrase()
spell that <user.letters>: user.dictation_insert(letters)
spell that <user.formatters> <user.letters>:
    result = user.formatted_text(letters, formatters)
    user.dictation_insert_raw(result)
