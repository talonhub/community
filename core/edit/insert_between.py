from time import sleep
from talon import Module, actions, settings

mod = Module()

mod.setting(
    "insert_between_wait",
    type=int,
    default=0,
    desc="Time in milliseconds to sleep after inserting text with `insert_between` (e.g. when using paired delimiters like 'box' or 'round'), before moving the cursor back. Useful to set on a per-application basis, to prevent moving the moving the cursor before text is inserted",
)

@mod.action_class
class module_actions:
    def insert_between(before: str, after: str):
        """Insert `before + after`, leaving cursor between `before` and `after`. Not entirely reliable if `after` contains newlines."""
        actions.insert(f"{before}{after}")
        sleep(int(settings.get("user.insert_between_wait", 0)) / 1000)
        for _ in after:
            actions.edit.left()
