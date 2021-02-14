from talon import Module, fs, Context
import os
import csv
from pathlib import Path
from typing import Dict, List, Tuple
import threading


# NOTE: This method requires this module to be one folder below the top-level
#   knausj folder.
SETTINGS_DIR = Path(__file__).parents[1] / "settings"

if not SETTINGS_DIR.is_dir():
    os.mkdir(SETTINGS_DIR)

mod = Module()
ctx = Context()


def _load_csv_dict(
    file_name: str, headers=Tuple[str, str], default: Dict[str, str] = {}
) -> Dict[str, str]:
    """Load a word mapping from a CSV file. If it doesn't exist, create it."""
    assert file_name.endswith(".csv")
    path = SETTINGS_DIR / file_name

    # Create the file if it doesn't exist
    if not SETTINGS_DIR.is_dir():
        os.mkdir(SETTINGS_DIR)
    if not path.is_file():
        with open(path, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for key, value in default.items():
                writer.writerow([key] if key == value else [value, key])

    # Now read from disk
    with open(path, "r", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    mapping = {}
    if len(rows) >= 2:
        actual_headers = rows[0]
        if not actual_headers == list(headers):
            print(
                f'"{file_name}": Malformed headers - {actual_headers}.'
                + f" Should be {list(headers)}. Ignoring row."
            )
        for row in rows[1:]:
            if len(row) == 0:
                # Windows newlines are sometimes read as empty rows. :champagne:
                continue
            if len(row) == 1:
                output = spoken_form = row[0]
            else:
                output, spoken_form = row[:2]
                if len(row) > 2:
                    print(
                        f'"{file_name}": More than two values in row: {row}.'
                        + " Ignoring the extras."
                    )
            # Leading/trailing whitespace in spoken form can prevent recognition.
            spoken_form = spoken_form.strip()
            mapping[spoken_form] = output
    return mapping


_mapped_lists = {}
_settings_lock = threading.Lock()
_word_map_params = None


def _update_list(list_name: str, *csv_params):
    """Update list with `list_name` from a csv on disk.

    `csv_params` will be passed to `_load_csv_dict`.

    """
    global ctx
    ctx.lists[list_name] = _load_csv_dict(*csv_params)


def _update_word_map(*csv_params):
    """Update `dictate.word_map` from disk.

    `csv_params` will be passed to `_load_csv_dict`.

    """
    global ctx
    ctx.settings["dictate.word_map"] = _load_csv_dict(*csv_params)


def _update_lists(*_):
    """Update all CSV lists from disk."""
    print("Updating CSV lists...")
    with _settings_lock:
        for list_name, csv_params in _mapped_lists.items():
            try:
                _update_list(list_name, *csv_params)
            except Exception as e:
                print(f'Error loading list "{list_name}": {e}')
        # Special case - `dictate.word_map` isn't a list.
        if _word_map_params:
            try:
                _update_word_map(*_word_map_params)
            except Exception as e:
                print(f'Error updating "dictate.word_map": {e}')


def bind_list_to_csv(
    list_name: str,
    csv_name: str,
    csv_headers: Tuple[str, str],
    default_values: Dict[str, str] = {},
) -> None:
    """Register a Talon list that should be updated from a CSV on disk.

    The CSV file will be created automatically in the "settings" dir if it
    doesn't exist. This directory can be tracked independently to
    `knausj_talon`, allowing the user to specify things like private vocab
    separately.

    Note the list must be declared separately.

    """
    global _mapped_lists
    with _settings_lock:
        _update_list(list_name, csv_name, csv_headers, default_values)
        # If there were no errors, we can register it permanently.
        _mapped_lists[list_name] = (csv_name, csv_headers, default_values)


def bind_word_map_to_csv(
    csv_name: str, csv_headers: Tuple[str, str], default_values: Dict[str, str] = {}
) -> None:
    """Like `bind_list_to_csv`, but for the `dictate.word_map` setting.

    Since it is a setting, not a list, it has to be handled separately.

    """
    global _word_map_params
    # TODO: Maybe a generic system for binding the dicts to settings? Only
    #   implement if it's needed.
    with _settings_lock:
        _update_word_map(csv_name, csv_headers, default_values)
        # If there were no errors, we can register it permanently.
        _word_map_params = (csv_name, csv_headers, default_values)


fs.watch(str(SETTINGS_DIR), _update_lists)
