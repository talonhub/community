import re
from dataclasses import dataclass

from talon import actions

INDENTATION = "    "
RE_STOP = re.compile(r"\$(\d+|\w+)|\$\{(\d+|\w+)\}|\$\{(\d+|\w+):(.+)\}")


@dataclass
class Stop:
    name: str
    rows_up: int
    row: int
    col: int


def insert_snippet_raw_text(body: str):
    """Insert snippet as raw text without editor support"""
    updated_snippet, stop = parse_snippet(body)

    actions.insert(updated_snippet)

    if stop:
        up(stop.rows_up)
        actions.edit.line_start()
        right(stop.col)


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
            stops.append(
                Stop(
                    name=match.group(1) or match.group(2) or match.group(3),
                    rows_up=len(lines) - i - 1,
                    row=i,
                    col=match.start(),
                )
            )

            # Remove tab stops and variables.
            stop_text = match.group(0)
            default_value = match.group(4) or ""
            line = line.replace(stop_text, default_value, 1)

            # Might have multiple stops on the same line
            match = RE_STOP.search(line)

        # Update existing line
        lines[i] = line

    updated_snippet = "\n".join(lines)

    return updated_snippet, get_first_stop(stops)


def up(n: int):
    """Move cursor up <n> rows"""
    for _ in range(n):
        actions.edit.up()


def right(n: int):
    """Move cursor right <n> columns"""
    for _ in range(n):
        actions.edit.right()


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
    return stops[0]
