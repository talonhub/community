from talon import Context, Module, actions

ctx = Context()
mod = Module()


@ctx.action_class("edit")
class EditActions:
    def paragraph_start():
        if extend_paragraph_start_with_success():
            actions.edit.left()

    def paragraph_end():
        if extend_paragraph_end_with_success():
            actions.edit.right()

    def select_paragraph():
        if is_line_empty():
            return
        # Search for start of paragraph
        actions.edit.extend_paragraph_start()
        actions.edit.left()
        # Extend to end of paragraph
        actions.edit.extend_paragraph_end()

    def extend_paragraph_start():
        # The reason for the wrapper function is a difference in function signature.
        # The Talon action has no return value and the below function returns a boolean with success state.
        extend_paragraph_start_with_success()

    def extend_paragraph_end():
        extend_paragraph_end_with_success()

    def delete_paragraph():
        actions.edit.select_paragraph()
        # Remove selection
        actions.edit.delete()
        # Remove the empty line containing the cursor
        actions.edit.delete()
        # Remove leading or trailing empty line
        actions.edit.delete_line()


@mod.action_class
class Actions:
    def cut_paragraph():
        """Cut paragraph under the cursor"""
        actions.edit.select_paragraph()
        actions.edit.cut()

    def copy_paragraph():
        """Copy paragraph under the cursor"""
        actions.edit.select_paragraph()
        actions.edit.copy()

    def paste_paragraph():
        """Paste to paragraph under the cursor"""
        actions.edit.select_paragraph()
        actions.edit.paste()


def is_line_empty() -> bool:
    """Check if the current line is empty. Return True if empty."""
    actions.edit.extend_line_start()
    text = actions.edit.selected_text().strip()
    if text:
        actions.edit.right()
        return False
    actions.edit.extend_line_end()
    text = actions.edit.selected_text().strip()
    if text:
        actions.edit.left()
        return False
    return True


def extend_paragraph_start_with_success() -> bool:
    """Extend selection to the start of the paragraph. Return True if successful."""
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    length = len(text)
    while True:
        actions.edit.extend_up()
        actions.edit.extend_line_start()
        text = actions.edit.selected_text()
        new_length = len(text)
        if new_length == length:
            break
        line = text[: new_length - length].strip()
        if not line:
            actions.edit.extend_down()
            break
        length = new_length
    return text.strip() != ""


def extend_paragraph_end_with_success() -> bool:
    """Extend selection to the end of the paragraph. Return True if successful."""
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    length = len(text)
    while True:
        actions.edit.extend_down()
        actions.edit.extend_line_end()
        text = actions.edit.selected_text()
        new_length = len(text)
        if new_length == length:
            break
        line = text[length:].strip()
        if not line:
            actions.edit.extend_line_start()
            actions.edit.extend_left()
            break
        length = new_length
    return text.strip() != ""
