# These are available when the draft window is open, but not necessarily focussed
tag: user.draft_window_showing
-
draft hide: user.draft_hide()

draft submit:
    content = user.draft_get_text()
    user.draft_hide()
    insert(content)
    # user.paste may be somewhat faster, but seems to be unreliable on MacOSX, see
    # https://github.com/talonvoice/talon/issues/254#issuecomment-789355238
    # user.paste(content)
