import csv
import logging
import os
import shutil
import warnings
from pathlib import Path
from typing import Dict, List, Tuple

from talon import resource

# NOTE: This method requires this module to be one folder below the top-level
#   knausj folder.
SETTINGS_DIR = Path(__file__).parents[1] / "settings"
DATA_DIR = Path(__file__).parents[1] / "data"

if not SETTINGS_DIR.is_dir():
    os.mkdir(SETTINGS_DIR)

if not DATA_DIR.is_dir():
    os.mkdir(DATA_DIR)


def get_list_from_csv(
    # the name of the csv
    filename: str,
    # the header, if any, for the CSV. None supported for back compat
    headers: Tuple[str, str] = None,
    # indicates whether or not the spoken form is first in the CSV format. For back compat.
    spoken_form_first=False,
    # indicates whether or not the leading and trailing whitespace should be stripped
    # from the result
    strip_whitepsace_from_output=False,
    # the legacy path. Path object expected. If it exists, it's moved to the settings folder
    legacy_path=None,
):
    """
    Retrieves list from CSV. 
    - Creates default CSV from template in /Data directory if it doesn't exist already
    - Uses resource.open so Talon reloads the script when the CSV is updated
    """
    path = SETTINGS_DIR / filename
    template_filename = filename + ".template"
    template_path = DATA_DIR / template_filename
    assert filename.endswith(".csv")

    if not path.is_file():
        # if a legacy path is specified and it exists,
        # move it
        if legacy_path and legacy_path.is_file():
            shutil.move(legacy_path, path)
            warnings.warn(
                "Support for the legacy CSVs location (i.e. outside /Settings) will be removed in the Talon v0.2.0 timeframe. Moving file from {} to {}".format(
                    legacy_path, path
                ),
                DeprecationWarning,
            )
        else:
            assert template_path.is_file()
            shutil.copyfile(template_path, path)

    # Now read via resource to take advantage of talon's
    # ability to reload this script for us when the resource changes
    with resource.open(str(path), "r") as f:
        rows = list(csv.reader(f))

    # print(str(rows))
    mapping = {}
    if len(rows) >= 2:
        # the start row for the actual contents, excluding the header
        start_row_index = 0

        if headers is not None:
            start_row_index = 1
            actual_headers = rows[0]
            if not actual_headers == list(headers):
                print(
                    f'"{filename}": Malformed headers - {actual_headers}.'
                    + f" Should be {list(headers)}. Ignoring row."
                )

        for row in rows[start_row_index:]:
            if len(row) == 0:
                # Windows newlines are sometimes read as empty rows. :champagne:
                continue
            if len(row) == 1:
                output = spoken_form = row[0]
            else:
                if spoken_form_first:
                    spoken_form, output = row[:2]
                else:
                    output, spoken_form = row[:2]

                if len(row) > 2:
                    print(
                        f'"{filename}": More than two values in row: {row}.'
                        + " Ignoring the extras."
                    )
            # Leading/trailing whitespace in spoken form can prevent recognition.
            spoken_form = spoken_form.strip()
            mapping[spoken_form] = (
                output.strip() if strip_whitepsace_from_output else output
            )

    return mapping
