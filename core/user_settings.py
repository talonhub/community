import csv
import io
import os
from pathlib import Path

from talon import resource

# NOTE: This method requires this module to be one folder below the top-level
#   community/knausj folder.
SETTINGS_DIR = Path(__file__).parents[1] / "settings"

if not SETTINGS_DIR.is_dir():
    os.mkdir(SETTINGS_DIR)


def get_list_from_csv(
    filename: str, headers: tuple[str, str], default: dict[str, str] = {}
):
    """Retrieves list from CSV"""
    path = SETTINGS_DIR / filename
    assert filename.endswith(".csv")

    if not path.is_file():
        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for key, value in default.items():
                writer.writerow([key] if key == value else [value, key])

    # Now read via resource to take advantage of talon's
    # ability to reload this script for us when the resource changes
    with resource.open(str(path), "r") as f:
        rows = list(csv.reader(f))

    # print(str(rows))
    mapping = {}
    if len(rows) >= 2:
        actual_headers = rows[0]
        if not actual_headers == list(headers):
            print(
                f'"{filename}": Malformed headers - {actual_headers}.'
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
                        f'"{filename}": More than two values in row: {row}.'
                        + " Ignoring the extras."
                    )
            # Leading/trailing whitespace in spoken form can prevent recognition.
            spoken_form = spoken_form.strip()
            mapping[spoken_form] = output

    return mapping


def append_to_csv(filename: str, rows: dict[str, str]):
    path = SETTINGS_DIR / filename
    assert filename.endswith(".csv")

    with open(str(path)) as file:
        line = None
        for line in file:
            pass
        needs_newline = line is not None and not line.endswith("\n")
    with open(path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if needs_newline:
            writer.writerow([])
        for key, value in rows.items():
            writer.writerow([key] if key == value else [value, key])


def get_key_value_pairs_and_spoken_forms_from_three_column_csv(
    filename: str, headers: tuple[str, str, str]
):
    """Retrieves a list from a CSV of the form name,values,spoken_forms"""
    path = compute_csv_path(filename)

    rows = _obtain_rows_from_csv(path)

    result = _convert_rows_from_file_with_headers_to_key_value_pairs_and_spoken_forms(
        rows, filename, headers
    )
    return result


def create_three_columns_csv_from_default_if_nonexistent(
    filename: str,
    headers: tuple[str, str, str],
    default: list[list[str, tuple[str], tuple[str]]],
):
    path = compute_csv_path(filename)
    if not path.is_file():
        _create_three_columns_csv_from_default(path, headers, default)


def _create_three_columns_csv_from_default(path, headers, default):
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row_tuple in default:
            row = _compute_row_for_three_column_csv(row_tuple)
            writer.writerow(row)


def _compute_row_for_three_column_csv(input_tuple):
    if len(input_tuple) == 3:
        name, values, spoken_forms = input_tuple
    else:
        name, values = input_tuple
        spoken_forms = None
    values_text = _compute_values_packed_into_column(values)
    row = [name, values_text]
    if spoken_forms:
        spoken_forms_text = _compute_values_packed_into_column(spoken_forms)
        row.append(spoken_forms_text)
    return row


def _compute_values_packed_into_column(values):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(values)
    result = output.getvalue().strip()
    return result


def _obtain_rows_from_csv(path):
    with open(str(path), "r", newline="") as f:
        rows = list(csv.reader(f))
    return rows


def _convert_rows_from_file_with_headers_to_key_value_pairs_and_spoken_forms(
    rows, filename, headers
):
    key_value_pairs = {}
    spoken_forms = {}
    if len(rows) >= 2:
        _complain_if_invalid_headers_found_in_file(rows, headers, filename)
        for row in rows[1:]:
            if len(row) == 0:
                # Windows newlines are sometimes read as empty rows. :champagne:
                continue
            elif len(row) == 1:
                print(f"{filename}: Ignoring row with only one value: {row}.")
                continue
            elif len(row) == 2:
                name, values_text = row
                new_spoken_forms_text = ""
            else:
                if len(row) > 3:
                    print(
                        f'"{filename}": More than three values in row: {row}.'
                        + " Ignoring the extras."
                    )
                name, values_text, new_spoken_forms_text = row[:3]
            name = name.strip()
            values = _get_intermediate_values_from_column(values_text)
            key_value_pairs[name] = values
            if new_spoken_forms_text:
                spoken_forms[name] = _get_spoken_forms_from_column(
                    new_spoken_forms_text
                )
    return key_value_pairs, spoken_forms


def _get_intermediate_values_from_column(values_text):
    reader = csv.reader([values_text], delimiter=";")
    values = next(reader)
    return values


def _get_spoken_forms_from_column(spoken_forms_text):
    reader = csv.reader([spoken_forms_text], delimiter=";")
    spoken_forms = next(reader)
    spoken_forms = [spoken_form.strip() for spoken_form in spoken_forms]
    return spoken_forms


def _complain_if_invalid_headers_found_in_file(rows, expected_headers, filename):
    actual_headers = rows[0]
    if not actual_headers == list(expected_headers):
        print(
            f'"{filename}": Malformed headers - {actual_headers}.'
            + f" Should be {list(expected_headers)}. Ignoring row."
        )


def compute_csv_path(filename: str):
    path = SETTINGS_DIR / filename
    assert filename.endswith(".csv")
    return path


def compute_spoken_form_to_key_dictionary(key_value_pairs, spoken_forms):
    if spoken_forms:
        result = {
            name: key
            for key in key_value_pairs
            for name in spoken_forms.get(key, [key])
        }
    else:
        result = {key: key for key in key_value_pairs}
    return result
