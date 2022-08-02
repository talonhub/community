-
#provide both anchored and unachored commands via 'over'
phrase <user.text>$:             user.insert_with_history(text)
phrase <user.text> over:         user.insert_with_history(text)
{user.prose_formatter} <user.prose>$:
    user.insert_formatted(prose, prose_formatter)
{user.prose_formatter} <user.prose> over:
    user.insert_formatted(prose, prose_formatter)
<user.format_text>+$:
    user.insert_many(format_text_list)
<user.format_text>+ over:
    user.insert_many(format_text_list)
<user.formatters> that:
    user.formatters_reformat_selection(user.formatters)
word <user.word>:
    user.insert_with_history(user.word)
recent list:
    user.toggle_phrase_history()
recent close:
    user.phrase_history_hide()
recent repeat <number_small>:
    user.insert_with_history(user.get_recent_phrase(number_small))
recent copy <number_small>:
    clip.set_text(user.get_recent_phrase(number_small))
select that:
    user.select_last_phrase()
before that:
    user.before_last_phrase()
nope that | scratch that:
    user.clear_last_phrase()
nope that was <user.formatters>:
    user.formatters_reformat_last(formatters)
