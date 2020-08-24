settings():
    user.screenshot_folder = "~/img/screenshots"
    user.screenshot_selection_command = "scrot -s"

^grab window$: user.screenshot_window()
^grab screen$: user.screenshot()
^grab selection$: user.screenshot_selection()
^grab window clip$: user.screenshot_window_clipboard()
^grab screen clip$: user.screenshot_clipboard()
