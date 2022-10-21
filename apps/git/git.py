import csv
import os
from pathlib import Path

from talon import Context, Module, actions, resource

mod = Module()
ctx = Context()

mod.list("git_command", desc="Git commands.")
mod.list("git_argument", desc="Command-line git options and arguments.")

dirpath = Path(__file__).parent
arguments_csv_path = str(dirpath / "git_arguments.csv")
commands_csv_path = str(dirpath / "git_commands.csv")


def make_list(path):
    with resource.open(path, "r") as f:
        rows = list(csv.reader(f))
    mapping = {}
    # ignore header row
    for row in rows[1:]:
        if len(row) == 0:
            continue
        if len(row) == 1:
            row = row[0], row[0]
        if len(row) > 2:
            print("{path!r}: More than two values in row: {row}. Ignoring the extras.")
        output, spoken_form = row[:2]
        spoken_form = spoken_form.strip()
        mapping[spoken_form] = output
    return mapping


ctx.lists["self.git_argument"] = make_list(arguments_csv_path)
ctx.lists["self.git_command"] = make_list(commands_csv_path)


@mod.capture(rule="{user.git_argument}+")
def git_arguments(m) -> str:
    """A non-empty sequence of git command arguments, preceded by a space."""
    return " " + " ".join(m.git_argument_list)
