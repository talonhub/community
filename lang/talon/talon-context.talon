tag: user.talonlist
tag: user.talon
tag: user.talon_python
-
#context requirements
win require: insert("os: windows\n")
mac require: insert("os: mac\n")
linux require: insert("os: linux\n")
title require: insert("win.title: ")
app [require] {user.talon_apps}:
    app = talon_apps or ""
    insert("app: {app}\n")
application [require] [{user.talon_apps}]:
    app = talon_apps or ""
    insert("app: {app}\n")
mode require [{user.talon_modes}]:
    mode = talon_modes or ""
    insert("mode: {mode}")
tag require [{user.talon_tags}]:
    tag = talon_tags or ""
    insert("tag: {tag}")
host require:
    hostname = user.talon_get_hostname()
    insert("hostname: {hostname}\n")
