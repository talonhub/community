import re
from collections import defaultdict
from dataclasses import dataclass

from talon import Module, actions, app, settings

mod = Module()


mod.setting(
    "snippet_raw_text_spaces_per_tab",
    type=int,
    default=4,
    desc="""The number of spaces per tab when inserting snippets as raw text. Set to -1 to insert tabs as tabs, such as in code editors that can expand tabs in pasted or typed text. This setting is provided for applications like web browsers and chat apps.""",
)

mod.setting(
    "snippet_raw_text_paste",
    type=bool,
    default=False,
    desc="""If true, inserting snippets as raw text will always be done through pasting""",
)

RE_STOP = re.compile(
    r"""
    (?:\\\$) (?# Escaped $ - not a stop; skip and don't capture anything)
    |
    (?:
        \$(\d+|\w+) (?# $... where ... is a captured stop number or variable)
        |
        \$\{(\d+|\w+)\} (?# ${...} where ... is as above)
        |
        \$\{(\d+|\w+):(.+)\} (?# ${...:xxx} where ... is as above and xxx a default value)
    )
    """,
    re.VERBOSE,
)

LAST_SNIPPET_HOLE_KEY_VALUE = 1000


@dataclass
class Stop:
    name: str
    rows_up: int
    columns_left: int
    row: int
    col: int

    def compute_sorting_key(self) -> int:
        """Returns a key value used to sort stops"""
        if self.name == "0":
            return LAST_SNIPPET_HOLE_KEY_VALUE
        if self.name.isdigit():
            return int(self.name)
        return 999


stop_stack: list[Stop] = []


def go_to_next_stop_raw():
    """Goes to the next snippet stop if it exists"""
    global stop_stack
    if len(stop_stack) > 1:
        current_stop = stop_stack.pop()
        next_stop = stop_stack[-1]
        move_to_correct_row(current_stop, next_stop)
        move_to_correct_column(next_stop)
    else:
        stop_stack = []


def insert_snippet_raw_text(body: str):
    """Insert snippet as raw text without editor support"""
    updated_snippet, stops = parse_snippet(body)
    sorted_stops = compute_stops_sorted_always_moving_left_to_right(stops)
    stop = get_first_stop(sorted_stops)

    update_stop_information(sorted_stops)

    if settings.get("user.snippet_raw_text_paste"):
        actions.user.paste(updated_snippet)
    else:
        actions.insert(updated_snippet)

    if stop:
        up(stop.rows_up)
        move_to_correct_column(stop)


def update_stop_information(stops: list[Stop]):
    global stop_stack
    if len(stops) > 1:
        stop_stack = stops[:]
        stop_stack.reverse()
    else:
        stop_stack = []


def compute_stops_sorted_always_moving_left_to_right(stops: list[Stop]) -> list[Stop]:
    """Without editor support, moving from right to left is problematic. Each line of stops is sorted by the smallest snippet hole key in the line. Each line gets sorted from left to right."""
    # Separate the stops by line keeping track of the smallest key in each line
    lines = defaultdict(list)
    smallest_keys = defaultdict(lambda: LAST_SNIPPET_HOLE_KEY_VALUE)
    for stop in stops:
        lines[stop.row].append(stop)
        line_key = smallest_keys[stop.row]
        smallest_keys[stop.row] = min(line_key, stop.compute_sorting_key())

    # If a line was from right to left, notify user and sort
    if is_any_line_from_right_to_left(lines.values()):
        app.notify(
            "The snippet you inserted got adjusted to move from left to right because editor support is unavailable."
        )
        sorted_stops: list[Stop] = []
        # Sort lines by key
        sorted_lines = sorted(
            lines.values(), key=lambda line: smallest_keys[line[0].row]
        )
        # Add every line sorted from left to right
        for line in sorted_lines:
            sorted_line = sorted(line, key=lambda stop: stop.col)
            sorted_stops.extend(sorted_line)
        return sorted_stops
    return sorted(stops, key=lambda stop: stop.compute_sorting_key())


def is_any_line_from_right_to_left(lines) -> bool:
    for line in lines:
        # Lines with only one stop are always in order
        if len(line) > 1:
            stop = line[0]
            stop_key = stop.compute_sorting_key()
            for next_stop in line[1:]:
                next_key = next_stop.compute_sorting_key()
                # If the ordering between the keys and columns are inconsistent,
                # the stops on this line go from right to left
                if (next_key < stop_key) != (next_stop.col < stop.col):
                    return True
                stop_key = next_key
                stop = next_stop
    return False


def move_to_correct_column(stop: Stop):
    actions.edit.line_end()
    move_cursor_left(stop.columns_left)


def move_to_correct_row(current_stop: Stop, next_stop: Stop):
    start = current_stop.row
    end = next_stop.row
    if start < end:
        for _ in range(end - start):
            actions.edit.down()
    elif start > end:
        for _ in range(start - end):
            actions.edit.up()


def format_tabs(text: str) -> str:
    """Possibly replaces tabs with spaces in the given text."""
    spaces_per_tab: int = settings.get("user.snippet_raw_text_spaces_per_tab")
    if spaces_per_tab < 0:
        return text
    return text.replace("\t", " " * spaces_per_tab)


def parse_snippet(body: str):
    # Some IM services will send the message on a tab
    body = format_tabs(body)

    lines = body.splitlines()
    stops: list[Stop] = []

    for i, line in enumerate(lines):
        start = 0
        while match := RE_STOP.search(line, start):
            stop_text = match.group(0)
            if stop_text[0] == "\\":
                # Remove escape for $
                value = stop_text[1:]
                # Don't match now-unescaped $ as a stop
                start = match.end() - 1
            else:
                name = match.group(1) or match.group(2) or match.group(3)
                value = match.group(4) or ""

                match name:
                    case "TM_SELECTED_TEXT":
                        value = actions.edit.selected_text() or value
                    case "CLIPBOARD":
                        value = actions.clip.text() or value
                    case _:
                        stops.append(
                            Stop(
                                name=name,
                                rows_up=len(lines) - i - 1,
                                columns_left=0,
                                row=i,
                                col=match.start(),
                            )
                        )

            # Remove/replace escaped $, tab stops and variables.
            line = line.replace(stop_text, value, 1)

        # Update existing line
        lines[i] = line

    # Can't calculate column left until line text is fully updated
    for stop in stops:
        stop.columns_left = len(lines[stop.row]) - stop.col

    updated_snippet = "\n".join(lines)

    return updated_snippet, stops


def up(n: int):
    """Move cursor up <n> rows"""
    for _ in range(n):
        actions.edit.up()


def move_cursor_left(n: int):
    """Move cursor left <n> columns"""
    for _ in range(n):
        actions.edit.left()


def get_first_stop(stops: list[Stop]):
    if not stops:
        return None
    stop = stops[0]
    if stop.rows_up == 0 and stop.columns_left == 0:
        return None
    return stop
