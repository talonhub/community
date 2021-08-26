from talon import Context, actions, ui, Module, app

mod = Module()

mod.apps.fish = """
app.name: fish
"""

mod.tag("fish", desc=".")
mod.apps.fish = """
tag: user.fish
"""


@mod.action_class
class Actions:
    def delete_big_word():
        """."""
        actions.edit.word_right()
        actions.key("ctrl-shift-w")

    def fuzzy_file():
        """."""
        pass
