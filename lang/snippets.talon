tag: user.snippets
-
snip {user.snippets}: user.snippet_insert(user.snippets)
snip hunt <user.text>: user.snippet_search(user.text)
snip hunt: user.snippet_search("")
snip create: user.snippet_create()
snip show: user.snippet_toggle()
