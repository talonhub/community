help alphabet: user.help_alphabet(user.get_alphabet())
help symbols: user.help_symbol_key_words(user.get_symbol_key_words())
help punctuation: user.help_punctuation_words(user.get_punctuation_words())
help modifier: user.help_modifier_words(user.get_modifier_words())
help simple keys: user.help_simple_keys(user.get_simple_keys())
help alternate keys:
	#these are keys that this script set has renamed to make more sense.  They are called 'alternate' because they rewrite the standard keyboard. 
	user.help_alternate_keys(user.get_alternate_keys())
help formatters:
	user.help_formatters(user.get_formatters_words())
help arrows:
	user.help_arrow_keys(user.get_arrow_keys())
help context$: user.help_context()
help active$: user.help_context_enabled()
help search <user.text>$: user.help_search(text)
help context {user.help_contexts}$: user.help_selected_context(help_contexts)
help help: user.help_search("help")
