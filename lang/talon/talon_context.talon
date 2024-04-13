code.language: talon
code.language: talonlist
code.language: python
and tag: user.talon_python
-
#context requirements
win require: insert("os: windows\n")
mac require: insert("os: mac\n")
linux require: insert("os: linux\n")
title require: insert("win.title: ")
application [require] [{user.talon_apps}]:
    app = "{talon_apps}\n" or ""
    insert("app: {app}")
mode require [{user.talon_modes}]:
    mode = "{talon_modes}\n" or ""
    insert("mode: {mode}")
tag require [{user.talon_tags}]:
    tag = "{talon_tags}\n" or ""
    insert("tag: {tag}")
host require:
    hostname = user.talon_get_hostname()
    insert("hostname: {hostname}\n")
