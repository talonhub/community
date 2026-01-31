from talon import Module, actions

mod = Module()

mod.tag(
    "line_commands",
    desc="Tag for enabling generic line navigation and selection commands",
)


@mod.action_class
class Actions:
    def extend_until_line(line: int):
        """Extends the selection from current line to the specified line"""

    def select_range(line_start: int, line_end: int):
        """Selects lines from line_start to line line_end"""
        actions.edit.jump_line(line_start)
        actions.edit.extend_line_end()

        number_of_lines = line_end - line_start
        for i in range(0, number_of_lines):
            actions.edit.extend_line_down()
        actions.edit.extend_line_end()

    def extend_camel_left():
        """Extends the selection by camel/subword to the left"""

    def extend_camel_right():
        """Extends the selection by camel/subword to the right"""

    def camel_left():
        """Moves cursor to the left by camel case/subword"""

    def camel_right():
        """Move cursor to the right by camel case/subword"""

    def line_clone(line: int):
        """Clones specified line at current position"""
        actions.edit.jump_line(line)
        actions.edit.line_clone()

    def jump_cursor_to_next_char(char: str):
        """Jumps the first to the next instance of the specified character on the current line"""

    def jump_cursor_to_prev_char(char: str):
        """Jumps the first to the previous instance of the specified character on the current line"""
