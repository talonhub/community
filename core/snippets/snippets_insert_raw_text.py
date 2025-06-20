import re
from dataclasses import dataclass
from collections import defaultdict

from talon import Module, actions, settings

mod = Module()

mod.setting(
    "snippet_raw_text_paste",
    type=bool,
    default=False,
    desc="""If true, inserting snippets as raw text will always be done through pasting""",
)

INDENTATION = "    "
RE_STOP = re.compile(r"\$(\d+|\w+)|\$\{(\d+|\w+)\}|\$\{(\d+|\w+):(.+)\}")
LAST_SNIPPET_HOLE_KEY_VALUE = 1000

@dataclass
class Stop:
    name: str
    rows_up: int
    columns_left: int
    row: int
    col: int


stop_stack: list[Stop] = []


def go_to_next_stop_raw():
    """Goes to the next snippet stop if it exists"""
    global stop_stack
    if len(stop_stack) > 1:
        current_stop = stop_stack.pop()
        next_stop = stop_stack[-1]
        if current_stop.row != next_stop.row:
            move_to_correct_row(current_stop.row, next_stop.row)
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
    #Separate the stops by line keeping track of the smallest key in each line
    lines = defaultdict(list)
    smallest_keys = defaultdict(lambda: LAST_SNIPPET_HOLE_KEY_VALUE)
    for stop in stops:
        lines[stop.row].append(stop)
        line_key = smallest_keys[stop.row]
        smallest_keys[stop.row] = min(line_key, key(stop))
                
    sorted_stops: list[Stop] = []
    #Sort lines by key
    sorted_lines = sorted(lines.values(), key=lambda line: smallest_keys[line[0].row])
    #Add every line sorted from left to right
    for line in sorted_lines:
        sorted_line = sorted(line, key=lambda stop: stop.col)
        sorted_stops.extend(sorted_line)
    return sorted_stops

def move_to_correct_column(stop: Stop):
    actions.edit.line_end()
    left(stop.columns_left)


def move_to_correct_row(start: int, end: int):
    if start < end:
        for _ in range(end - start):
            actions.edit.down()
    else:
        for _ in range(start - end):
            actions.edit.up()


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
        return LAST_SNIPPET_HOLE_KEY_VALUE
    if stop.name.isdigit():
        return int(stop.name)
    return 999


def get_first_stop(stops: list[Stop]):
    if not stops:
        return None
    stop = stops[0]
    if stop.rows_up == 0 and stop.columns_left == 0:
        return None
    return stop
