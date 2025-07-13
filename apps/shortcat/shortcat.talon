^(shot | sot) [<user.text>]: user.shortcat_hover(text or "")

^(shot | sot) click [<user.text>]:
    # Add some delay to cancel click if needed
    user.shortcat_click(text or "", "1500ms")

^(shot | sot) right [<user.text>]:
    # Add some delay to cancel right-click if needed
    user.shortcat_right(text or "", "1500ms")

^(shot | sot) dub [<user.text>]:
    # Add some delay to cancel double-click if needed
    user.shortcat_double_click(text or "", "1500ms")
