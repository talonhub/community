from talon import Module, actions

mod = Module()


@mod.action_class
class module_actions:
    def insert_between(before: str, after: str):
        """Insert `before + after`, leaving cursor between `before` and `after`. Not entirely reliable if `after` contains newlines."""
        actions.insert(f"{before}{after}")
        for _ in after:
            actions.edit.left()
