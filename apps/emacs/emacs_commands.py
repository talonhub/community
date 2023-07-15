import csv
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, Optional

from talon import Context, Module, actions, app, resource

mod = Module()
mod.list("emacs_command", desc="Emacs commands")

ctx = Context()


class Command(NamedTuple):
    name: str
    keys: Optional[str] = None
    short: Optional[str] = None
    spoken: Optional[str] = None


# Maps command name to Command.
emacs_commands = {}


@mod.action_class
class Actions:
    def emacs_command_keybinding(command_name: str) -> Optional[str]:
        "Looks up the keybinding for command_name in emacs_commands.csv."
        return emacs_commands.get(command_name, Command(command_name)).keys

    def emacs_command_short_form(command_name: str) -> Optional[str]:
        "Looks up the short form for command_name in emacs_commands.csv."
        return emacs_commands.get(command_name, Command(command_name)).short


def load_csv():
    filepath = Path(__file__).parents[0] / "emacs_commands.csv"
    with resource.open(filepath) as f:
        rows = list(csv.reader(f))
    # Check headers
    assert rows[0] == ["Command", " Key binding", " Short form", " Spoken form"]

    commands = []
    for row in rows[1:]:
        if 0 == len(row):
            continue
        if len(row) > 4:
            print(
                f'"{filepath}": More than four values in row: {row}. '
                + " Ignoring the extras"
            )
        name, keys, short, spoken = (
            [x.strip() or None for x in row] + [None, None, None]
        )[:4]
        commands.append(Command(name=name, keys=keys, short=short, spoken=spoken))

    # Update global command info.
    global emacs_commands
    emacs_commands = {c.name: c for c in commands}

    # Generate spoken forms and apply overrides.
    try:
        command_list = actions.user.create_spoken_forms_from_list(
            [c.name for c in commands], generate_subsequences=False
        )
    except:
        pass
    else:
        for c in commands:
            if c.spoken:
                command_list[c.spoken] = c.name
    ctx.lists["self.emacs_command"] = command_list


# TODO: register on change to file!
app.register("ready", load_csv)
