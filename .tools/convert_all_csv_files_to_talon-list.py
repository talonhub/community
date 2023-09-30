# This script needs to be executed from the ".tools/" directory

import os
from pathlib import Path

known_csv_files = {
    "apps/emacs/emacs_commands.csv": {},
    "apps/git/git_arguments.csv": {},
    "apps/git/git_commands.csv": {},
    "core/app_switcher/app_name_overrides.linux.csv": {},
    "core/app_switcher/app_name_overrides.mac.csv": {},
    "core/app_switcher/app_name_overrides.windows.csv": {},
    "core/homophones/homophones.csv": {},
    "settings/abbreviations.csv": {},
    "settings/additional_words.csv": {},
    "settings/alphabet.csv": {
        "name": "user.letter",
        "newpath": "core/keys/letter.talon-list",
    },
    "settings/file_extensions.csv": {},
    "settings/search_engines.csv": {},
    "settings/system_paths.csv": {},
    "settings/unix_utilities.csv": {},
    "settings/websites.csv": {},
    "settings/words_to_replace.csv": {},
    "tags/emoji/emoji.csv": {},
    "tags/emoji/emoticon.csv": {},
    "tags/emoji/kaomoji.csv": {},
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
        file.readline()
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
    output = []

    output.append(f"list: {config['name']}")
    output.append("-")

    for line in lines:
        if not line.strip():
            continue

        key, value = line.split(",")
        output.append(f"{value}:\t{key}")

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


def main():
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
        talonlist_relative_file = normalize_path(config["newpath"])
        talonlist_file = os.path.join(directory_to_search, talonlist_relative_file)
        if os.path.isfile(talonlist_file) and not os.path.isfile(csv_file):
            print(f"Skipping existing talon-file {talonlist_relative_file}")
            continue
        if os.path.isfile(disabled_csv_file):
            print(
                f"Skipping existing renamed csv file {strip_base_directory(disabled_csv_file)}"
            )
            continue
        print(
            f"Converting csv file: {csv_relative_file} -> talon-list file: {talonlist_relative_file}"
        )
        csv_content = read_csv_file(csv_file)
        talonlist_content = convert_format_csv_to_talonlist(csv_content, config)
        # print(talonlist_content)

        write_to_file(talonlist_file, talonlist_content)
        os.rename(csv_file, disabled_csv_file)


if __name__ == "__main__":
    main()
