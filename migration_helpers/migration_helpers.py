import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from talon import Module, actions, app

mod = Module()


# custom function to format emoticon.csv values. quick and dirty.
def emoticon_value_converter(value):
    return f'"""{value}"""'


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
        "apps/git/git_arguments.csv",
        "apps/git/git_argument.talon-list",
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.git_command",
        "apps/git/git_commands.csv",
        "apps/git/git_command.talon-list",
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.vocabulary",
        "settings/additional_words.csv",
        "core/vocabulary/vocabulary.talon-list",
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.letter",
        "settings/alphabet.csv",
        "core/keys/letter.talon-list",
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.system_paths",
        "settings/system_paths.csv",
        lambda: f"core/system_paths-{actions.user.talon_get_hostname()}.talon-list",
        True,
        False,
        (lambda: f"host: {actions.user.talon_get_hostname()}"),
        None,
    ),
    CSVData(
        "user.search_engine",
        "settings/search_engines.csv",
        "core/websites_and_search_engines/search_engine.talon-list",
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.unix_utility",
        "settings/unix_utilities.csv",
        "tags/terminal/unix_utility.talon-list",
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.website",
        "settings/websites.csv",
        "core/websites_and_search_engines/website.talon-list",
        True,
        False,
        None,
        None,
    ),
    CSVData(
        "user.emoji",
        "tags/emoji/emoji.csv",
        "tags/emoji/emoji.talon-list",
        False,
        True,
        None,
        None,
    ),
    CSVData(
        "user.emoticon",
        "tags/emoji/emoticon.csv",
        "tags/emoji/emoticon.talon-list",
        False,
        True,
        None,
        emoticon_value_converter,
    ),
    CSVData(
        "user.kaomoji",
        "tags/emoji/kaomoji.csv",
        "tags/emoji/kaomoji.talon-list",
        False,
        True,
        None,
        None,
    ),
]


def normalize_path(path_string):
    """
    Normalize a path based on the current operating system.

    Args:
    - path_string (str): The path string to be normalized.

    Returns:
    - str: A normalized path string appropriate for the current OS.
    """
    return str(Path(path_string))


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


def parent_directory_of_script():
    """
    Get the parent directory of the currently executing Python script.

    Returns:
    - Path: A `Path` object representing the parent directory of the current script.

    Note:
    This function is intended to be called from within a script and may not
    work as expected if called interactively (e.g., from a Python REPL).

    Example:
    Assuming the script is located at "/home/user/scripts/myscript.py":
    >>> parent_directory_of_script()
    Path("/home/user/scripts")
    """
    # Get the directory of the current Python script
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    parent_dir = script_dir.parent
    return parent_dir


def find_csv_files(directory):
    """
    Finds all files with a .csv extension within the specified directory and its subdirectories.

    This function follows symbolic links but skips directories and their contents if any directory
    in the path starts with a period (".").

    Args:
        directory (str): The starting directory for the search.

    Returns:
        list: List of file paths with a .csv extension, relative to the given directory.

    Example:
        >>> find_csv_files('./data')
        ['sample1.csv', 'subfolder/sample2.csv']
    """
    csv_files = []

    for dirpath, dirnames, filenames in os.walk(directory, followlinks=True):
        # Skip directories that start with a '.'
        if any(
            dir_component.startswith(".") for dir_component in dirpath.split(os.sep)
        ):
            continue

        for filename in filenames:
            # ignore if the .csv file starts with a "." since it indicates an already converted .csv into .talon-list
            if filename.endswith(".csv") and not filename.startswith("."):
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, directory)
                csv_files.append(relative_path)

    return csv_files


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


def get_new_absolute_path(absolute_path):
    """
    Return the new absolute path for a file by changing to .csv-converted

    Args:
    - absolute_path (str): The absolute path to the file.

    Returns:
    - str: The new absolute path after changing to .csv-converted
    """
    dir_name = os.path.dirname(absolute_path)
    base_filename = os.path.basename(absolute_path)

    # Construct the new absolute path
    new_absolute_path = os.path.join(
        dir_name, base_filename.replace(".csv", ".csv-converted")
    )

    return new_absolute_path


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
    known_csv_files = {normalize_path(item.path): item for item in csv_files_list}
    conversion_count = 0
    directory_to_search = parent_directory_of_script()

    print(f"migration_helpers.py convert_files - Base directory: {directory_to_search}")
    csv_relative_files_list = find_csv_files(directory_to_search)

    for csv_relative_file in csv_relative_files_list:
        csv_file = os.path.join(directory_to_search, csv_relative_file)
        disabled_csv_file = get_new_absolute_path(csv_file)
        if csv_relative_file not in known_csv_files.keys():
            print(f"Skipping unsupported csv file {csv_relative_file}")
            continue
        config = known_csv_files[csv_relative_file]
        if not config:
            print(f"Skipping currently unsupported conversion: {csv_relative_file}")
            continue

        if callable(config.newpath):
            newpath = config.newpath()
        else:
            newpath = config.newpath

        talonlist_relative_file = normalize_path(newpath)
        talonlist_file = os.path.join(directory_to_search, talonlist_relative_file)

        if os.path.isfile(talonlist_file) and not os.path.isfile(csv_file):
            print(f"Skipping existing talon-file {talonlist_relative_file}")
            continue

        if disabled_csv_file and os.path.isfile(disabled_csv_file):
            print(f"Skipping existing renamed csv file {disabled_csv_file}")
            continue

        print(
            f"Converting csv file: {csv_relative_file} -> talon-list file: {talonlist_relative_file}"
        )

        conversion_count += 1
        csv_content = read_csv_file(csv_file)
        talonlist_content = convert_format_csv_to_talonlist(csv_content, config)

        write_to_file(talonlist_file, talonlist_content)
        os.rename(csv_file, disabled_csv_file)

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
