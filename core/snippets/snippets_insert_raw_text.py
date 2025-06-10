import re
from dataclasses import dataclass

from talon import Module, actions, settings

mod = Module()


mod.setting(
    "snippet_raw_text_spaces_per_tab",
    type=int,
    default=4,
    desc="""The number of spaces to use for each tab in snippets inserted as raw text when converting tabs to spaces. A negative value prevents tabs from getting converted spaces.""",
)

RE_STOP = re.compile(r"\$(\d+|\w+)|\$\{(\d+|\w+)\}|\$\{(\d+|\w+):(.+)\}")


@dataclass
class Stop:
    name: str
    rows_up: int
    columns_left: int
    row: int
    col: int


def insert_snippet_raw_text(body: str):
    """Insert snippet as raw text without editor support"""
    updated_snippet, stop = parse_snippet(body)

    actions.insert(updated_snippet)

    if stop:
        up(stop.rows_up)
        actions.edit.line_end()
        left(stop.columns_left)


def compute_indentation_as_spaces():
    return " " * settings.get("user.snippets_raw_text_spaces_per_tab")


def parse_snippet(body: str):
    # Some IM services will send the message on a tab
    if settings.get("user.snippets_raw_text_spaces_per_tab") >= 0:
        body = re.sub(r"\t", compute_indentation_as_spaces(), body)

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
                    columns_left=0,
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

    # Can't calculate column left until line text is fully updated
    for stop in stops:
        stop.columns_left = len(lines[stop.row]) - stop.col

    updated_snippet = "\n".join(lines)

    return updated_snippet, get_first_stop(stops)


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
