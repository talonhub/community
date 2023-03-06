app: vivaldi
-
tag(): browser
tag(): user.tabs

(sidebar | panel) history: user.vivaldi_history_panel()
(sidebar | panel) downloads: user.vivaldi_downloads_panel()
(sidebar | panel) bookmarks: user.vivaldi_bookmarks_panel()
(sidebar | panel) notes: user.vivaldi_notes_panel()

please [<user.text>]:
    user.vivaldi_toggle_quick_commands()
    sleep(180ms)
    insert(user.text or "")
