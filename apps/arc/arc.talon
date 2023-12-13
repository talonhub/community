app: arc
-
tag(): browser
tag(): user.tabs

please [<user.text>]:
    user.command_palette()
    sleep(200ms)
    insert(user.text or "")
