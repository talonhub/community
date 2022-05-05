mode: command
mode: dictation
-
copy to vocab [as <phrase>]$: user.add_selection_to_vocabulary(phrase or "")
copy name to vocab [as <phrase>]$: user.add_selection_to_vocabulary(phrase or "", "name")
copy noun to vocab [as <phrase>]$: user.add_selection_to_vocabulary(phrase or "", "noun")
copy to replacements as <phrase>$: user.add_selection_to_words_to_replace(phrase)
copy name to replacements as <phrase>$: user.add_selection_to_words_to_replace(phrase, "name")
copy noun to replacements as <phrase>$: user.add_selection_to_words_to_replace(phrase, "noun")
