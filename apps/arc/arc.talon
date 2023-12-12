app: arc
-
tag(): browser
tag(): user.tabs

please [<user.text>]:
    user.command_palette()
    actions.sleep("180ms")
    insert(user.text or "")
