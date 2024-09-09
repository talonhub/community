import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from talon import Module, actions, app

mod = Module()


@dataclass
class CSVData:
    """Class to track CSV-related data necessary for conversion to .talon-list"""

    # name of the list
    name: str
    # Path to the CSV file
    path: str
    # path to the generated .talon-list
    newpath: Union[str, callable] = None
    # Indicates whether the first line of the CSV file is a header
    # that should be ignored
    is_first_line_header: bool = True
    # Indicates whether the spoken form or value is first in the CSV file
    is_spoken_form_first: bool = False
    # An optional callable for generating a custom header for
    # generated .talon-list
    custom_header: callable = None
    # An optional callable for custom processing of the value for
    # generated .talon-list
    custom_value_converter: callable = None


# Note: homophones, emacs_commands, file_extensions, words_to_replace, abbreviations, and app name overrides
# are intentionally omitted, as their use cases are not compatible with .talon-list conversions
supported_csv_files = [
    CSVData(
        "user.git_argument",
        os.path.join("apps", "git", "git_arguments.csv"),
        os.path.join("apps", "git", "git_argument.talon-list"),
    ),
    CSVData(
        "user.git_command",
        os.path.join("apps", "git", "git_commands.csv"),
        os.path.join("apps", "git", "git_command.talon-list"),
    ),
    CSVData(
        "user.vocabulary",
        os.path.join("settings", "additional_words.csv"),
        os.path.join("core", "vocabulary", "vocabulary.talon-list"),
    ),
    CSVData(
        "user.letter",
        os.path.join("settings", "alphabet.csv"),
        os.path.join("core", "keys", "letter.talon-list"),
    ),
    CSVData(
        "user.system_paths",
        os.path.join("settings", "system_paths.csv"),
        lambda: os.path.join(
            "core", f"system_paths-{actions.user.talon_get_hostname()}.talon-list"
        ),
        custom_header=(lambda: f"hostname: {actions.user.talon_get_hostname()}"),
    ),
    CSVData(
        "user.search_engine",
        os.path.join("settings", "search_engines.csv"),
        os.path.join("core", "websites_and_search_engines", "search_engine.talon-list"),
    ),
    CSVData(
        "user.unix_utility",
        os.path.join("settings", "unix_utilities.csv"),
        os.path.join("tags", "terminal", "unix_utility.talon-list"),
    ),
    CSVData(
        "user.website",
        os.path.join("settings", "websites.csv"),
        os.path.join("core", "websites_and_search_engines", "website.talon-list"),
    ),
    CSVData(
        "user.emoji",
        os.path.join("tags", "emoji", "emoji.csv"),
        os.path.join("tags", "emoji", "emoji.talon-list"),
        is_first_line_header=False,
        is_spoken_form_first=True,
    ),
    CSVData(
        "user.emoticon",
        os.path.join("tags", "emoji", "emoticon.csv"),
        os.path.join("tags", "emoji", "emoticon.talon-list"),
        is_first_line_header=False,
        is_spoken_form_first=True,
    ),
    CSVData(
        "user.kaomoji",
        os.path.join("tags", "emoji", "kaomoji.csv"),
        os.path.join("tags", "emoji", "kaomoji.talon-list"),
        is_first_line_header=False,
        is_spoken_form_first=True,
    ),
]


def convert_csv_to_talonlist(input_csv: csv.reader, config: CSVData):
    """
    Convert a 1 or 2 column CSV into a talon list.
    Empty lines, lines containing only whitespace or starting with a # are skipped.

    Args:
    - input_csv: A csv.reader instance
    - config: A CSVData instance

    Returns:
    - str: The contents of a talon list file

    Raises:
    - ValueError: If any line in the input CSV contains more than 2 columns.
    """
    rows = list(input_csv)

    is_spoken_form_first = config.is_spoken_form_first
    is_first_line_header = config.is_first_line_header
    start_index = 1 if is_first_line_header else 0
    output = []

    output.append(f"list: {config.name}")
    if config.custom_header and callable(config.custom_header):
        output.append(config.custom_header())

    output.append("-")

    for row in rows[start_index:]:
        # Remove trailing whitespace for each cell
        row = [col.rstrip() for col in row]
        cols = len(row)

        # Check columns
        if cols > 2:
            raise ValueError("Expected only 1 or 2 columns, got {cols}:", row)

        # Exclude empty or comment rows
        if cols == 0 or (cols == 1 and row[0] == "") or row[0].startswith("#"):
            continue

        if cols == 2:
            if is_spoken_form_first:
                spoken_form, value = row
            else:
                value, spoken_form = row

            if config.custom_value_converter:
                value = config.custom_value_converter(value)

        else:
            spoken_form = value = row[0]

        if spoken_form != value:
            if not str.isprintable(value) or "'" in value or '"' in value:
                value = repr(value)

            output.append(f"{spoken_form}: {value}")
        else:
            output.append(f"{spoken_form}")

    # Terminate file in newline
    output.append("")
    return "\n".join(output)


def convert_files(csv_files_list):
    known_csv_files = {str(item.path): item for item in csv_files_list}

    conversion_count = 0
    base_path = Path(__file__).resolve().parent.parent

    for csv_path in base_path.rglob("*.csv"):
        csv_relative_path = csv_path.relative_to(base_path)
        migrated_csv_path = csv_path.with_suffix(".csv-converted-to-talon-list")

        config = known_csv_files.get(str(csv_relative_path))
        if not config:
            continue

        if callable(config.newpath):
            talonlist_relative_path = config.newpath()
        else:
            talonlist_relative_path = config.newpath

        talonlist_path = base_path / talonlist_relative_path

        if talonlist_path.is_file() and not csv_path.is_file():
            print(f"Skipping existing Talon list file {talonlist_relative_path}")
            continue

        if migrated_csv_path.is_file():
            print(f"Skipping existing renamed CSV {migrated_csv_path}")
            continue

        print(
            f"Converting CSV {csv_relative_path} to Talon list {talonlist_relative_path}"
        )

        conversion_count += 1
        with open(csv_path, newline="") as csv_file:
            csv_reader = csv.reader(csv_file, skipinitialspace=True)
            talonlist_content = convert_csv_to_talonlist(csv_reader, config)

        print(
            f"Renaming converted CSV to {migrated_csv_path.name}. This file may be deleted if no longer needed; it's preserved in case there's an issue with conversion."
        )
        if talonlist_path.is_file():
            backup_path = talonlist_path.with_suffix(".bak")
            print(
                f"Migration target {talonlist_relative_path} already exists; backing up to {backup_path}"
            )
            talonlist_path.rename(backup_path)

        with open(talonlist_path, "w") as talonlist_file:
            talonlist_file.write(talonlist_content)
        csv_path.rename(migrated_csv_path)

    return conversion_count


@mod.action_class
class Actions:
    def migrate_known_csv_files():
        """Migrate known CSV files to .talon-list"""
        conversion_count = convert_files(supported_csv_files)
        if conversion_count > 0:
            notification_text = f"migration_helpers.py converted {conversion_count} CSVs. See Talon log for more details.\n"
            print(notification_text)
            actions.app.notify(notification_text)

    def migrate_custom_csv(
        path: str,
        new_path: str,
        list_name: str,
        is_first_line_header: bool,
        spoken_form_first: bool,
    ):
        """Migrate a custom CSV file"""
        csv_file = CSVData(
            list_name,
            path,
            new_path,
            is_first_line_header,
            spoken_form_first,
            None,
            None,
        )
        convert_files([csv_file])


def on_ready():
    try:
        actions.user.migrate_known_csv_files()
    except KeyError:
        # Due to a core Talon bug, the above action may not be available when a ready callback is invoked.
        # (see https://github.com/talonhub/community/pull/1268#issuecomment-2325721706)
        notification = (
            "Unable to migrate CSVs to Talon lists.",
            "Please quit and restart Talon.",
        )
        app.notify(*notification)
        print(*notification)


app.register("ready", on_ready)
