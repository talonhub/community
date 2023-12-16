app: arc
os: mac
-
tag(): browser
tag(): user.tabs

please [<user.text>]:
    key("cmd-l")
    sleep(200ms)
    insert(user.text or "")
