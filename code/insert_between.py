from talon import Module, actions, app

mod = Module()


@mod.action_class
class module_actions:
    def insert_between(before: str, after: str):
        """Insert `before + after`, leaving cursor between `before` and `after`. Not entirely reliable if `after` contains newlines."""
        actions.insert(before + after)
        for _ in after:
            actions.edit.left()

    # This is deprecated, please use insert_between instead.
    def insert_cursor(text: str):
        """Insert a string. Leave the cursor wherever [|] is in the text"""
        if "[|]" in text:
            actions.user.insert_between(*text.split("[|]", 1))
        else:
            actions.insert(text)
        app.notify(
            "insert_cursor is deprecated, please update your code to use insert_between"
        )
