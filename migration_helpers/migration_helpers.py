import os
import re
from pathlib import Path

from talon import Module, actions, app

mod = Module()


# custom function to format emoticon.csv values. quick and dirty.
def emoticon_value_converter(value):
    return f'"""{value}"""'


known_csv_files = {
    # emacs_commands likely needs to remain a csv
    # "apps/emacs/emacs_commands.csv": {},
    "apps/git/git_arguments.csv": {
        "name": "user.git_argument",
        "newpath": "apps/git/git_argument.talon-list",
        "is_spoken_form_first": False,
        "is_first_line_header": True,
    },
    "apps/git/git_commands.csv": {
        "name": "user.git_command",
        "newpath": "apps/git/git_command.talon-list",
        "is_spoken_form_first": False,
        "is_first_line_header": True,
    },
    # there's no way currently to migrate this without using
    # registry.list
    # "core/app_switcher/app_name_overrides.linux.csv": {
    # "is_spoken_form_first": True,
    # },
    # there's no way currently to migrate this without using
    # registry.list
    # "core/app_switcher/app_name_overrides.mac.csv": {
    # "is_spoken_form_first": True,
    # },
    # "core/app_switcher/app_name_overrides.windows.csv": {
    # "is_spoken_form_first": True,
    # },
    # homophones needs to remain a csv, as it is a one-to-many mapping
    # "core/homophones/homophones.csv": {},
    # abbreviations is currently used by create_spoken_forms
    # and requires additional work to port.
    # Likely needs to remain a CSV
    # "settings/abbreviations.csv": {
    # "name": "user.abbreviation",
    # "newpath": "core/abbreviate/abbreviation.talon-list",
    # "is_spoken_form_first": False,
    # },
    "settings/additional_words.csv": {
        "name": "user.vocabulary",
        "newpath": "core/vocabulary/vocabulary.talon-list",
        "is_spoken_form_first": False,
        "is_first_line_header": True,
    },
    "settings/alphabet.csv": {
        "name": "user.letter",
        "newpath": "core/keys/letter.talon-list",
        "is_spoken_form_first": False,
        "is_first_line_header": True,
    },
    # file_extensions is currently used by create_spoken_forms
    # and requires additional care to port
    # Likely needs to remain a CSV
    # "settings/file_extensions.csv": {
    # "name": "user.file_extension"
    # "newpath": "core/file_extension/file_extension.talon-list",
    # },
    "settings/search_engines.csv": {
        "name": "user.search_engine",
        "newpath": "core/websites_and_search_engines/search_engine.talon-list",
        "is_spoken_form_first": False,
        "is_first_line_header": True,
    },
    # system paths is likely host-specific
    # and should be treated as such
    "settings/system_paths.csv": {
        "name": "user.system_paths",
        "newpath": (
            lambda: f"core/system_paths-{actions.user.talon_get_hostname()}.talon-list"
        ),
        "is_spoken_form_first": False,
        "is_first_line_header": True,
        "custom_header": (lambda: f"host: {actions.user.talon_get_hostname()}"),
    },
    "settings/unix_utilities.csv": {
        "name": "user.unix_utility",
        "newpath": "tags/terminal/unix_utility.talon-list",
        "is_spoken_form_first": False,
        "is_first_line_header": True,
    },
    "settings/websites.csv": {
        "name": "user.website",
        "newpath": "core/websites_and_search_engines/website.talon-list",
        "is_spoken_form_first": False,
        "is_first_line_header": True,
    },
    # words to replace is a setting in talon
    # not sure how to handle this.
    # "settings/words_to_replace.csv": {},
    "tags/emoji/emoji.csv": {
        "name": "user.emoji",
        "newpath": "tags/emoji/emoji.talon-list",
        "is_spoken_form_first": True,
        "is_first_line_header": False,
    },
    # due to the characters in emoticons
    # this needs special handling
    "tags/emoji/emoticon.csv": {
        "name": "user.emoticon",
        "newpath": "tags/emoji/emoticon.talon-list",
        "is_spoken_form_first": True,
        "is_first_line_header": False,
        "custom_value_converter": emoticon_value_converter,
    },
    # due to the characters in kaomoji
    # this needs special handling
    "tags/emoji/kaomoji.csv": {
        "name": "user.kaomoji",
        "newpath": "tags/emoji/kaomoji.talon-list",
        "is_spoken_form_first": True,
        "is_first_line_header": False,
    },
}


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


def convert_format_csv_to_talonlist(input_string, config):
    """
    Convert a string with lines of "value,key" pairs into a format of "key:\tvalue" pairs.
    Empty lines or lines containing only whitespace are skipped.

    Args:
    - input_string (str): A multi-line string where each line is expected to be in "value,key" format.
    Returns:
    - str: A reformatted multi-line string in "key:\tvalue" format.

    Raises:
    - ValueError: If any line in the input string does not contain exactly one comma separator.

    Example:
    >>> convert_format_csv_to_talonlist("a,air\n\nb,bat")
    'air:\ta\nbat:\tb'

    Note:
    The function assumes that each non-empty line in the input string has exactly one comma
    separating a value and a key. Lines that don't meet this criterion will raise an error.
    """
    lines = input_string.split("\n")
    is_spoken_form_first = config["is_spoken_form_first"]
    is_first_line_header = config["is_first_line_header"]
    start_index = 1 if is_first_line_header else 0
    output = []

    output.append(f"list: {config['name']}")
    if config.get("custom_header"):
        output.append(config.get("custom_header")())

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
            if config.get("custom_value_converter"):
                value = config["custom_value_converter"](value)

        else:
            spoken_form = value = line.strip()

        spoken_form = spoken_form.strip()
        output.append(f"{spoken_form}: {value}")

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


def get_new_absolute_path_by_prefixing_dot(absolute_path):
    """
    Return the new absolute path for a file by prefixing its base name with a "."

    Args:
    - absolute_path (str): The absolute path to the file.

    Returns:
    - str: The new absolute path after prefixing the base name with ".".
    """
    dir_name = os.path.dirname(absolute_path)
    base_filename = os.path.basename(absolute_path)

    # Prefix the base filename with "."
    new_filename = "." + base_filename

    # Construct the new absolute path
    new_absolute_path = os.path.join(dir_name, new_filename)

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


def convert_files():
    global known_csv_files
    known_csv_files = {
        normalize_path(key): value for key, value in known_csv_files.items()
    }

    directory_to_search = parent_directory_of_script()
    print(f"Base directory: {directory_to_search}")
    csv_relative_files_list = find_csv_files(directory_to_search)

    for csv_relative_file in csv_relative_files_list:
        csv_file = os.path.join(directory_to_search, csv_relative_file)
        disabled_csv_file = get_new_absolute_path_by_prefixing_dot(csv_file)
        if csv_relative_file not in known_csv_files.keys():
            print(f"Skipping non default csv file {csv_relative_file}")
            continue
        config = known_csv_files[csv_relative_file]
        if not config:
            print(f"Skipping unsuppported convertion yet: {csv_relative_file}")
            continue

        if callable(config["newpath"]):
            newpath = config["newpath"]()
        else:
            newpath = config["newpath"]

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
        csv_content = read_csv_file(csv_file)
        talonlist_content = convert_format_csv_to_talonlist(csv_content, config)
        # print(talonlist_content)

        write_to_file(talonlist_file, talonlist_content)
        os.rename(csv_file, disabled_csv_file)


@mod.action_class
class MigrationActions:
    def migrate_known_csv_files():
        """migrates known CSV files to .talon-list"""
        convert_files()

    def migrate_custom_csv(
        path: str, new_path: str, list_name: str, spoken_form_first: bool
    ):
        """Migrates custom CSV files"""


def on_ready():
    convert_files()


app.register("ready", on_ready)
