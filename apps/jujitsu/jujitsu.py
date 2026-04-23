import csv
import os
from pathlib import Path

from talon import Context, Module, resource

mod = Module()
ctx = Context()

mod.list("jujitsu_command", desc="jujitsu commands.")
mod.list("jujitsu_argument", desc="Command-line jujitsu options and arguments.")

dirpath = Path(__file__).parent
arguments_csv_path = str(dirpath / "jujitsu_arguments.csv")
commands_csv_path = str(dirpath / "jujitsu_commands.csv")


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


ctx.lists["self.jujitsu_argument"] = make_list(arguments_csv_path)
ctx.lists["self.jujitsu_command"] = make_list(commands_csv_path)


@mod.capture(rule="{user.jujitsu_argument}+")
def jujitsu_arguments(m) -> str:
    """A non-empty sequence of jujitsu command arguments, preceded by a space."""
    return " " + " ".join(m.jujitsu_argument_list)
