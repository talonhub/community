# If you do not want snippets inserted with an added stop at the end: Uncomment the following line and comment the line after it
#snip {user.snippet}: user.insert_snippet_by_name(snippet)
snip {user.snippet}: user.insert_snippet_by_name_with_stop_at_end(snippet)

# If you do not want phrase snippet insertion to add a stop at the end: Uncomment the line 2 lines down and comment the line after it
snip {user.snippet_with_phrase} <user.text>:
    #user.insert_snippet_by_name_with_phrase(snippet_with_phrase, text)
    user.insert_snippet_by_name_with_phrase_and_stop_at_end(snippet_with_phrase, text)

snip next: user.move_cursor_to_next_snippet_stop()
