# These are available globally (in command mode)
mode: command
-
^draft show:
    # Do this toggle so we can have focus when saying 'draft show'
    user.draft_hide()
    user.draft_show()

^draft show <user.draft_window_position>:
    # Do this toggle so we can have focus when saying 'draft show'
    user.draft_hide()
    user.draft_show()
    user.draft_named_move(draft_window_position)

^draft show small:
    # Do this toggle so we can have focus when saying 'draft show'
    user.draft_hide()
    user.draft_show()
    user.draft_resize(600, 200)

^draft show large:
    # Do this toggle so we can have focus when saying 'draft show'
    user.draft_hide()
    user.draft_show()
    user.draft_resize(800, 500)

^draft empty: user.draft_show("")

^draft edit:
    text = edit.selected_text()
    key(backspace)
    user.draft_show(text)

^draft edit all:
    edit.select_all()
    text = edit.selected_text()
    key(backspace)
    user.draft_show(text)
