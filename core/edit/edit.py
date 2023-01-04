from talon import Context, Module, actions, clip

ctx = Context()
mod = Module()

PUNCTUATION_SYMBOLS_WHICH_SIGNIFY_THE_END_OF_A_WORD = \
    ['.', '!', '?', ';', ':', '—', '_', '/', '\\', '|',
     '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']',
     '{', '}', '<', '>', '=', '+', '-', '~', '`', ' ', '']

@ctx.action_class("edit")
class EditActions:
    def selected_text() -> str:
        with clip.capture() as s:
            actions.edit.copy()
        try:
            return s.text()
        except clip.NoChange:
            return ""

    def line_insert_down():
        actions.edit.line_end()
        actions.key("enter")

    def selection_clone():
        actions.edit.copy()
        actions.edit.select_none()
        actions.edit.paste()

    def line_clone():
        # This may not work if editor auto-indents. Is there a better way?
        actions.edit.line_start()
        actions.edit.extend_line_end()
        actions.edit.copy()
        actions.edit.right()
        actions.key("enter")
        actions.edit.paste()

    def select_word():
        actions.edit.extend_right()
        character_to_right_of_initial_caret_position = actions.edit.selected_text()
        actions.edit.left()

        # .strip() is to handle newline characters
        if (character_to_right_of_initial_caret_position.strip() in
                PUNCTUATION_SYMBOLS_WHICH_SIGNIFY_THE_END_OF_A_WORD):
            actions.edit.extend_word_left()
        else:
            actions.edit.word_right()
            actions.edit.extend_word_left()


@mod.action_class
class Actions:
    def paste(text: str):
        """Pastes text and preserves clipboard"""

        with clip.revert():
            clip.set_text(text)
            actions.edit.paste()
            # sleep here so that clip.revert doesn't revert the clipboard too soon
            actions.sleep("150ms")

    def words_left(n: int):
        """Moves left by n words."""
        for _ in range(n):
            actions.edit.word_left()

    def words_right(n: int):
        """Moves right by n words."""
        for _ in range(n):
            actions.edit.word_right()

    def cut_word_left():
        """Cuts the word to the left."""
        actions.edit.extend_word_left()
        actions.edit.cut()

    def cut_word_right():
        """Cuts the word to the right."""
        actions.edit.extend_word_right()
        actions.edit.cut()

    def cut_line():
        """Cuts the current line."""
        actions.edit.select_line()
        actions.edit.cut()

    def copy_word_left():
        """Copies the word to the left."""
        actions.edit.extend_word_left()
        actions.edit.copy()

    def copy_word_right():
        """Copies the word to the right."""
        actions.edit.extend_word_right()
        actions.edit.copy()
