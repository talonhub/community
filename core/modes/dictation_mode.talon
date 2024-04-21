mode: dictation
-
settings():
    user.context_sensitive_dictation = true 
    
# ^press <user.modifiers>$: key(modifiers)
# ^press <user.keys>$: key(keys)

# Everything here should call `auto_insert()` (instead of `insert()`), to preserve the state to correctly auto-capitalize/auto-space.
# (Talonscript string literals implicitly call `auto_insert`, so there's no need to wrap those)
<user.raw_prose>: user.dictation_insert(raw_prose)
# cap: user.dictation_format_cap()

