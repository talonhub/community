from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag("edit", desc="Custom edit actions")


@mod.action_class
class UserEditActions:
    def delete_word_left():
        """Delete word to the right of the cursor"""
        actions.key("alt-backspace")

    def delete_word_right():
        """Delete word to the left of the cursor"""
        actions.key("alt-delete")
