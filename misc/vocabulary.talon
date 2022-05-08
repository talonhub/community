mode: command
mode: dictation
-
copy to vocab [as <phrase>]$: user.add_selection_to_vocabulary(phrase or "")
# Automatically adds possessive form by appending "'s".
copy name to vocab [as <phrase>]$: user.add_selection_to_vocabulary(phrase or "", "name")
# Automatically adds plural form by simply appending "s".
copy noun to vocab [as <phrase>]$: user.add_selection_to_vocabulary(phrase or "", "noun")
copy to replacements as <phrase>$: user.add_selection_to_words_to_replace(phrase)
# Automatically adds possessive form by appending "'s".
copy name to replacements as <phrase>$: user.add_selection_to_words_to_replace(phrase, "name")
# Automatically adds plural form by simply appending "s".
copy noun to replacements as <phrase>$: user.add_selection_to_words_to_replace(phrase, "noun")
