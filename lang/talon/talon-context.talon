tag: user.talonlist
tag: user.talon
tag: user.talon_python
-
#context requirements
win require: user.paste("os: windows\n")
mac require: user.paste("os: mac\n")
linux require: user.paste("os: linux\n")
title require: user.paste("win.title: ")
application [require] [{user.talon_apps}]:
    app = talon_apps or ""
    user.paste("app: {app}")
mode require [{user.talon_modes}]:
    mode = talon_modes or ""
    user.paste("mode: {mode}")
tag require [{user.talon_tags}]:
    tag = talon_tags or ""
    user.paste("tag: {tag}")
host require:
    hostname = user.talon_get_hostname()
    user.paste("hostname: {hostname}\n")


