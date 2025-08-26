#snip {user.snippet}: user.insert_snippet_by_name(snippet)
snip {user.snippet}: user.insert_snippet_by_name_with_stop_at_end(snippet)

snip {user.snippet_with_phrase} <user.text>:
    user.insert_snippet_by_name_with_phrase(snippet_with_phrase, text)

snip next: user.move_cursor_to_next_snippet_stop()
