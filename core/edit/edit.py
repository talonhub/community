from talon import Context, Module, actions, clip

ctx = Context()
mod = Module()

END_OF_WORD_SYMBOLS = ".!?;:—_/\\|@#$%^&*()[]{}<>=+-~`"


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

    # # This simpler implementation of select_word mostly works, but in some apps it doesn't.
    # # See https://github.com/talonhub/community/issues/1084.
    # def select_word():
    #     actions.edit.right()
    #     actions.edit.word_left()
    #     actions.edit.extend_word_right()

    def select_word():
        actions.edit.extend_right()
        character_to_right_of_initial_caret_position = actions.edit.selected_text()

        # Occasionally apps won't let you edit.extend_right()
        # and therefore won't select text if your caret is on the rightmost character
        # such as in the Chrome URL bar
        did_select_text = character_to_right_of_initial_caret_position != ""

        if did_select_text:
            # .strip() turns newline & space characters into empty string; the empty
            # string is in any other string, so this works.
            if (
                character_to_right_of_initial_caret_position.strip()
                in END_OF_WORD_SYMBOLS
            ):
                # Come out of the highlight in the initial position.
                actions.edit.left()
            else:
                # Come out of the highlight one character
                # to the right of the initial position.
                actions.edit.right()

        actions.edit.word_left()
        actions.edit.extend_word_right()


@mod.action_class
class Actions:
    def paste(text: str):
        """Pastes text and preserves clipboard"""

        with clip.revert():
            clip.set_text(text)
            actions.edit.paste()
            # sleep here so that clip.revert doesn't revert the clipboard too soon
            actions.sleep("150ms")

    def delete_right():
        """Delete character to the right"""
        actions.key("delete")

    def words_left(n: int):
        """Moves left by n words."""
        for _ in range(n):
            actions.edit.word_left()

    def words_right(n: int):
        """Moves right by n words."""
        for _ in range(n):
            actions.edit.word_right()

    def cut_word():
        """Cut word under cursor"""
        actions.edit.select_word()
        actions.edit.cut()

    def cut_word_left():
        """Cuts the word to the left."""
        actions.edit.extend_word_left()
        actions.edit.cut()

    def cut_word_right():
        """Cuts the word to the right."""
        actions.edit.extend_word_right()
        actions.edit.cut()

    def copy_word():
        """Copy word under cursor"""
        actions.edit.select_word()
        actions.edit.copy()

    def copy_word_left():
        """Copies the word to the left."""
        actions.edit.extend_word_left()
        actions.edit.copy()

    def copy_word_right():
        """Copies the word to the right."""
        actions.edit.extend_word_right()
        actions.edit.copy()

    def paste_word():
        """Paste to word under cursor"""
        actions.edit.select_word()
        actions.edit.paste()

    def cut_all():
        """Cut all text in the current document"""
        actions.edit.select_all()
        actions.edit.cut()

    def copy_all():
        """Copy all text in the current document"""
        actions.edit.select_all()
        actions.edit.copy()

    def paste_all():
        """Paste to the current document"""
        actions.edit.select_all()
        actions.edit.paste()

    def delete_all():
        """Delete all text in the current document"""
        actions.edit.select_all()
        actions.edit.delete()

    def cut_line():
        """Cut current line"""
        actions.edit.select_line()
        actions.edit.cut()

    def copy_line():
        """Copy current line"""
        actions.edit.select_line()
        actions.edit.copy()

    def paste_line():
        """Paste to current line"""
        actions.edit.select_line()
        actions.edit.paste()

    # ----- Start / End of line -----
    def select_line_start():
        """Select to start of current line"""
        if actions.edit.selected_text():
            actions.edit.left()
        actions.edit.extend_line_start()

    def select_line_end():
        """Select to end of current line"""
        if actions.edit.selected_text():
            actions.edit.right()
        actions.edit.extend_line_end()

    def cut_line_start():
        """Cut to start of current line"""
        actions.user.select_line_start()
        actions.edit.cut()

    def cut_line_end():
        """Cut to end of current line"""
        actions.user.select_line_end()
        actions.edit.cut()

    def copy_line_start():
        """Copy to start of current line"""
        actions.user.select_line_start()
        actions.edit.copy()

    def copy_line_end():
        """Copy to end of current line"""
        actions.user.select_line_end()
        actions.edit.copy()

    def paste_line_start():
        """Paste to start of current line"""
        actions.user.select_line_start()
        actions.edit.paste()

    def paste_line_end():
        """Paste to end of current line"""
        actions.user.select_line_end()
        actions.edit.paste()

    def delete_line_start():
        """Delete to start of current line"""
        actions.user.select_line_start()
        actions.edit.delete()

    def delete_line_end():
        """Delete to end of current line"""
        actions.user.select_line_end()
        actions.edit.delete()
