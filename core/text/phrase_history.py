import logging

from talon import Module, actions, imgui

mod = Module()

# list of recent phrases, most recent first
phrase_history = []
phrase_history_length = 40
phrase_history_display_length = 40


@mod.action_class
class Actions:
    def get_last_phrase() -> str:
        """Gets the last phrase"""
        return phrase_history[0] if phrase_history else ""

    def get_recent_phrase(number: int) -> str:
        """Gets the nth most recent phrase"""
        try:
            return phrase_history[number - 1]
        except IndexError:
            return ""

    def clear_last_phrase():
        """Clears the last phrase"""
        # Currently, this removes the cleared phrase from the phrase history, so
        # that repeated calls clear successively earlier phrases, which is often
        # useful. But it would be nice if we could do this without removing
        # those phrases from the history entirely, so that they were still
        # accessible for copying, for example.
        if not phrase_history:
            logging.warning("clear_last_phrase(): No last phrase to clear!")
            return
        for _ in phrase_history.pop(0):
            actions.key("backspace")

    def select_last_phrase():
        """Selects the last phrase"""
        if not phrase_history:
            logging.warning("select_last_phrase(): No last phrase to select!")
            return
        for _ in phrase_history[0]:
            actions.edit.extend_left()

    def before_last_phrase():
        """Moves left before the last phrase"""
        try:
            for _ in phrase_history.pop(0):
                actions.edit.left()
        except IndexError:
            logging.warning("before_last_phrase(): No last phrase to move before!")

    def add_phrase_to_history(text: str):
        """Adds a phrase to the phrase history"""
        global phrase_history
        phrase_history.insert(0, text)
        phrase_history = phrase_history[:phrase_history_length]

    def toggle_phrase_history():
        """Toggles list of recent phrases"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def phrase_history_hide():
        """Hides the recent phrases window"""

        gui.hide()


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Recent phrases")
    gui.text("Say 'recent repeat <number>' retype a phrase on this list.")
    gui.text("Say 'recent copy <number>' to copy a phrase from this list.")
    gui.line()
    for index, text in enumerate(phrase_history[:phrase_history_display_length], 1):
        gui.text(f"{index}: {text}")

    gui.spacer()
    if gui.button("Recent close"):
        actions.user.phrase_history_hide()
