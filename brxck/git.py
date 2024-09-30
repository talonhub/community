import os

from talon import actions

os.system("git fetch origin")
code = os.system("cd ./user/brxck_talon && git diff --exit-code origin/main")

if code != 0:
    actions.app.notify(
        "New changes available in brxck_talon",
        "Talon config update",
    )
