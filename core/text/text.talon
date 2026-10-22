#provide both anchored and unachored commands via 'over'
phrase <user.text>$:
    user.add_phrase_to_history(text)
    insert(text)
phrase <user.text> {user.phrase_ender}:
    user.add_phrase_to_history(text)
    insert("{text}{phrase_ender}")
{user.prose_formatter} <user.prose>$: user.insert_formatted(prose, prose_formatter)
{user.prose_formatter} <user.prose> {user.phrase_ender}:
    user.insert_formatted(prose, prose_formatter)
    insert(phrase_ender)
<user.format_code>+$: user.insert_many(format_code_list)
<user.format_code>+ {user.phrase_ender}:
    user.insert_many(format_code_list)
    insert(phrase_ender)
<user.formatters> that: user.formatters_reformat_selection(user.formatters)
{user.word_formatter} <user.word>: user.insert_formatted(word, word_formatter)
<user.formatters> (pace | paste): user.insert_formatted(clip.text(), formatters)
recent list: user.toggle_phrase_history()
recent close: user.phrase_history_hide()
recent repeat <number_small>:
    recent_phrase = user.get_recent_phrase(number_small)
    user.add_phrase_to_history(recent_phrase)
    insert(recent_phrase)
recent copy <number_small>: clip.set_text(user.get_recent_phrase(number_small))
select that: user.select_last_phrase()
before that: user.before_last_phrase()
nope that | scratch that: user.clear_last_phrase()
nope that was <user.formatters>: user.formatters_reformat_last(formatters)
(abbreviate | abreviate | brief) {user.abbreviation}: "{abbreviation}"
<user.formatters> (abbreviate | abreviate | brief) {user.abbreviation}:
    user.insert_formatted(abbreviation, formatters)
