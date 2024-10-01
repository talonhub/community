import os

from talon import actions

code = os.system(
    (
        "cd ./user/brxck_talon &&"
        "git fetch origin main &&"
        "[ $(git rev-list HEAD..origin/main --count) -ne 0 ] &&"
        "exit 1 || exit 0"
    )
)

if code != 0:
    actions.app.notify(
        "New changes available in brxck_talon",
        "Talon config update",
    )
