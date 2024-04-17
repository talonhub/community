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
        os.path.normpath("apps/git/git_arguments.csv"),
        os.path.normpath("apps/git/git_argument.talon-list"),
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.git_command",
        os.path.normpath("apps/git/git_commands.csv"),
        os.path.normpath("apps/git/git_command.talon-list"),
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.vocabulary",
        os.path.normpath("settings/additional_words.csv"),
        os.path.normpath("core/vocabulary/vocabulary.talon-list"),
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.letter",
        os.path.normpath("settings/alphabet.csv"),
        os.path.normpath("core/keys/letter.talon-list"),
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.system_paths",
        os.path.normpath("settings/system_paths.csv"),
        lambda: os.path.normpath(
            f"core/system_paths-{actions.user.talon_get_hostname()}.talon-list"
        ),
        True,
        False,
        (lambda: f"host: {actions.user.talon_get_hostname()}"),
        None,
    ),
    CSVData(
        "user.search_engine",
        os.path.normpath("settings/search_engines.csv"),
        os.path.normpath("core/websites_and_search_engines/search_engine.talon-list"),
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.unix_utility",
        os.path.normpath("settings/unix_utilities.csv"),
        os.path.normpath("tags/terminal/unix_utility.talon-list"),
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.website",
        os.path.normpath("settings/websites.csv"),
        os.path.normpath("core/websites_and_search_engines/website.talon-list"),
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.emoji",
        os.path.normpath("tags/emoji/emoji.csv"),
        os.path.normpath("tags/emoji/emoji.talon-list"),
        False,
        True,
        None,
        None,
    ),
    CSVData(
        "user.emoticon",
        os.path.normpath("tags/emoji/emoticon.csv"),
        os.path.normpath("tags/emoji/emoticon.talon-list"),
        False,
        True,
        None,
        None,
    ),
    CSVData(
        "user.kaomoji",
        os.path.normpath("tags/emoji/kaomoji.csv"),
        os.path.normpath("tags/emoji/kaomoji.talon-list"),
        False,
        True,
        None,
        None,
    ),
]


def read_csv_file(file_name):
    """
    Read the content of a text file while skipping its first line.

    Args:
    - file_name (str): Path to the text file to be read.

    Returns:
    - str: The content of the file after skipping the first line.

    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - IOError: For other I/O related errors, such as issues with file permissions.

    Example:
    Assuming the content of 'sample.txt' is:
    Line 1
    Line 2
    Line 3

    >>> read_csv_file('sample.txt')
    'Line 2\nLine 3\n'
    """
    with open(file_name, "r") as file:
        # Skip the first line
        return file.read()


def convert_format_csv_to_talonlist(input_string: str, config: CSVData):
    """
    Convert a string with lines of "value,key" pairs into a format of "key: value" pairs.
    Empty lines or lines containing only whitespace are skipped.

    Args:
    - input_string (str): A multi-line string where each line is expected to be in "value,key" format.
    - config: CSVData instance

    Returns:
    - str: A reformatted multi-line string in "key: value" format.

    Raises:
    - ValueError: If any line in the input string does not contain exactly one comma separator.

    Example:
    >>> convert_format_csv_to_talonlist("a,air\n\nb,bat")
    'air: a\nbat: b'

    Note:
    The function assumes that each non-empty line in the input string has exactly one comma
    separating a value and a key. Lines that don't meet this criterion will raise an error.
    """
    lines = input_string.split("\n")
    is_spoken_form_first = config.is_spoken_form_first
    is_first_line_header = config.is_first_line_header
    start_index = 1 if is_first_line_header else 0
    output = []

    output.append(f"list: {config.name}")
    if config.custom_header and callable(config.custom_header):
        output.append(config.custom_header())

    output.append("-")

    for line in lines[start_index:]:
        if len(line) == 0 or line[0] == "#":
            continue

        if not line.strip():
            continue

        if "," in line:
            if is_spoken_form_first:
                spoken_form, value = line.split(",")
            else:
                value, spoken_form = line.split(",")

            value = value.strip()
            if config.custom_value_converter:
                value = config.custom_value_converter(value)

            # escape various characters... very rudimentary
            else:
                value = repr(value)

        else:
            spoken_form = value = line.strip()

        spoken_form = spoken_form.strip()
        if spoken_form != value:
            output.append(f"{spoken_form}: {value}")
        else:
            output.append(f"{spoken_form}")

    return "\n".join(output)


def write_to_file(filename, text):
    """
    Write a text string into a specified file.

    Args:
    - filename (str): The path of the file where the text should be written.
    - text (str): The text to be written to the file.

    Returns:
    - None
    """
    with open(filename, "w") as file:
        file.write(text)


def strip_base_directory(base_dir, path):
    """
    Strip the base directory from the path if it exists.

    Parameters:
    - base_dir (str): The base directory to be stripped.
    - path (str): The path from which the base directory should be stripped.

    Returns:
    - str: Path after stripping the base directory.
    """

    # Ensure both the base directory and path are normalized
    base_dir = os.path.normpath(base_dir)
    path = os.path.normpath(path)

    # Check if the path starts with the base directory
    if path.startswith(base_dir):
        # Subtract base_dir length from path
        return path[len(base_dir) :].lstrip(os.sep)  # Remove any leading separators
    else:
        return path


def convert_files(csv_files_list):
    global known_csv_files
    known_csv_files = {os.path.normpath(item.path): item for item in csv_files_list}

    conversion_count = 0
    base_directory = os.path.dirname(os.path.dirname(__file__))

    print(f"migration_helpers.py convert_files - Base directory: {base_directory}")
    for csv_file in Path(base_directory).rglob("*.csv"):
        csv_file_path = os.path.normpath(csv_file.resolve())
        csv_relative_file_path = os.path.normpath(csv_file.relative_to(base_directory))
        migrated_csv_file_path = csv_file_path.replace(".csv", ".csv-converted")

        if csv_relative_file_path not in known_csv_files.keys():
            print(f"Skipping unsupported csv file {csv_relative_file_path}")
            continue

        config = known_csv_files[csv_relative_file_path]
        if not config:
            print(
                f"Skipping currently unsupported conversion: {csv_relative_file_path}"
            )
            continue

        if callable(config.newpath):
            newpath = config.newpath()
        else:
            newpath = config.newpath

        talonlist_relative_file = os.path.normpath(newpath)
        talonlist_file = os.path.join(base_directory, talonlist_relative_file)

        if os.path.isfile(talonlist_file) and not os.path.isfile(csv_file):
            print(f"Skipping existing talon-file {talonlist_relative_file}")
            continue

        if migrated_csv_file_path and os.path.isfile(migrated_csv_file_path):
            print(f"Skipping existing renamed csv file {migrated_csv_file_path}")
            continue

        print(
            f"Converting csv file: {csv_relative_file_path} -> talon-list file: {talonlist_relative_file}"
        )

        conversion_count += 1
        csv_content = read_csv_file(csv_file)
        talonlist_content = convert_format_csv_to_talonlist(csv_content, config)

        print(
            f"Renaming converted csv file: {csv_file_path} -> {migrated_csv_file_path}. This file may be deleted if no longer needed; provided for reference in case there's an issue"
        )
        if os.path.isfile(talonlist_file):
            backup_file_name = talonlist_file.replace(".talon-list", ".bak")
            print(f"Migration target {talonlist_relative_file} already exists, backing up to {backup_file_name}")
            os.rename(talonlist_file, backup_file_name)
            
        write_to_file(talonlist_file, talonlist_content)
        os.rename(csv_file_path, migrated_csv_file_path)

    return conversion_count


@mod.action_class
class MigrationActions:
    def migrate_known_csv_files():
        """migrates known CSV files to .talon-list"""
        conversion_count = convert_files(supported_csv_files)
        if conversion_count > 0:
            notification_text = f"migrations_helpers.py converted {conversion_count} CSVs. See Talon log for more details. \n"
            print(notification_text)
            actions.app.notify(notification_text)

    def migrate_custom_csv(
        path: str,
        new_path: str,
        list_name: str,
        is_first_line_header: bool,
        spoken_form_first: bool,
    ):
        """Migrates custom CSV files"""
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
    actions.user.migrate_known_csv_files()


app.register("ready", on_ready)
