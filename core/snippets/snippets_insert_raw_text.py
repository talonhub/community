import re
from dataclasses import dataclass

from talon import actions

INDENTATION = "    "
RE_STOP = re.compile(r"\$(\d+|\w+)|\$\{(\d+|\w+)\}|\$\{(\d+|\w+):(.+)\}")


@dataclass
class Stop:
    name: str
    rows_up: int
    columns_left: int
    row: int
    col: int


stop_stack: list[Stop] | None = None


def update_stop_information(stops: list[Stop]):
    global stop_stack
    if len(stops) > 1:
        stop_stack = stops
        stop_stack.reverse()
    else:
        stop_stack = None


def move_to_correct_column(start: int, end: int):
    if start < end:
        for _ in range(end - start):
            actions.edit.right()
    else:
        for _ in range(start - end):
            actions.edit.left()


def move_to_correct_row(start: int, end: int):
    if start < end:
        for _ in range(end - start):
            actions.edit.down()
    else:
        for _ in range(start - end):
            actions.edit.up()


def go_to_next_stop():
    """Goes to the next snippet stop if it exists"""
    global stop_stack

    if stop_stack:
        current_stop = stop_stack.pop()
        next_stop = stop_stack[-1]
        if current_stop.row == next_stop.row:
            move_to_correct_column(current_stop.col, next_stop.col)
        else:
            move_to_correct_row(current_stop.row, next_stop.row)
            actions.edit.line_end()
            left(next_stop.columns_left)
        if len(stop_stack) <= 1:
            stop_stack = None


def insert_snippet_raw_text(body: str):
    """Insert snippet as raw text without editor support"""
    updated_snippet, stops = parse_snippet(body)
    stop = get_first_stop(stops)

    update_stop_information(stops)

    actions.insert(updated_snippet)

    if stop:
        up(stop.rows_up)
        actions.edit.line_end()
        left(stop.columns_left)


def parse_snippet(body: str):
    # Some IM services will send the message on a tab
    body = re.sub(r"\t", INDENTATION, body)

    # Replace variable with appropriate value/text
    body = re.sub(r"\$TM_SELECTED_TEXT", lambda _: actions.edit.selected_text(), body)
    body = re.sub(r"\$CLIPBOARD", lambda _: actions.clip.text(), body)

    lines = body.splitlines()
    stops: list[Stop] = []

    for i, line in enumerate(lines):
        match = RE_STOP.search(line)

        while match:
            # Remove tab stops and variables.
            stop_text = match.group(0)
            default_value = match.group(4) or ""
            line = line.replace(stop_text, default_value, 1)

            stops.append(
                Stop(
                    name=match.group(1) or match.group(2) or match.group(3),
                    rows_up=len(lines) - i - 1,
                    columns_left=len(line) - match.start(),
                    row=i,
                    col=match.start(),
                )
            )

            # Might have multiple stops on the same line
            match = RE_STOP.search(line)

        # Update existing line
        lines[i] = line

    updated_snippet = "\n".join(lines)

    return updated_snippet, stops


def up(n: int):
    """Move cursor up <n> rows"""
    for _ in range(n):
        actions.edit.up()


def left(n: int):
    """Move cursor left <n> columns"""
    for _ in range(n):
        actions.edit.left()


def key(stop: Stop):
    if stop.name == "0":
        return 1000
    if stop.name.isdigit():
        return int(stop.name)
    return 999


def get_first_stop(stops: list[Stop]):
    if not stops:
        return None
    stops.sort(key=key)
    stop = stops[0]
    if stop.rows_up == 0 and stop.columns_left == 0:
        return None
    return stop
