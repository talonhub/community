import re

from talon import actions


def insert_snippet_raw_text(body: str):
    """Insert snippet as raw text without editor support"""
    lines = body.splitlines()
    found_stop = False

    for i, line in enumerate(lines):
        # Some IM services will send the message on a tab
        line = re.sub(r"\t+", "    ", line)

        if found_stop != "$1":
            if "$1" in line:
                found_stop = "$1"
                stop_row = i
                stop_col = line.index("$1")
            elif "$0" in line:
                found_stop = "$0"
                stop_row = i
                stop_col = line.index("$0")

        # Replace placeholders with default text
        line = re.sub(r"\$\{\d+:(.*?)\}", r"\1", line)
        # Remove tab stops
        line = re.sub(r"\$\d+", "", line)
        # Update existing line
        lines[i] = line

    updated_snippet = "\n".join(lines)
    actions.insert(updated_snippet)

    if found_stop:
        up(len(lines) - stop_row - 1)
        actions.edit.line_start()
        right(stop_col)


def up(n: int):
    """Move cursor up <n> rows"""
    for _ in range(n):
        actions.edit.up()


def right(n: int):
    """Move cursor right <n> columns"""
    for _ in range(n):
        actions.edit.right()
