import os

from talon import actions, app

code = os.system(
    (
        "cd ./user/brxck_talon &&"
        "git fetch origin main &&"
        "[ $(git rev-list HEAD..origin/main --count) -ne 0 ] &&"
        "exit 1 || exit 0"
    )
)

def notify_changes():
    if code != 0:
        actions.app.notify(
            "New changes in brxck_talon",
            "Update config",
        )

app.register("ready", notify_changes)
