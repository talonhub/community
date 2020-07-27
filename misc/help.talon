-
settings():
    user.help_max_contexts_per_page = 20
    user.help_max_command_lines_per_page = 50

help alphabet: user.help_alphabet(user.get_alphabet())
help context$: user.help_context()
help active$: user.help_context_enabled()
help search <user.text>$: user.help_search(text)
help context <user.help_contexts>$: user.help_selected_context(user.help_contexts)


