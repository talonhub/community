import csv
import os
from pathlib import Path
from typing import IO, Callable

from talon import resource

# NOTE: This method requires this module to be one folder below the top-level
#   community folder.
SETTINGS_DIR = Path(__file__).parents[1] / "settings"
SETTINGS_DIR.mkdir(exist_ok=True)

CallbackT = Callable[[dict[str, str]], None]
DecoratorT = Callable[[CallbackT], CallbackT]


def read_csv_list(
    f: IO, headers: tuple[str, str], is_spoken_form_first: bool = False
) -> dict[str, str]:
    rows = list(csv.reader(f))

    # print(str(rows))
    mapping = {}
    if len(rows) >= 2:
        actual_headers = rows[0]
        if not actual_headers == list(headers):
            print(
                f'"{f.name}": Malformed headers - {actual_headers}.'
                + f" Should be {list(headers)}. Ignoring row."
            )
        for row in rows[1:]:
            if len(row) == 0:
                # Windows newlines are sometimes read as empty rows. :champagne:
                continue
            if len(row) == 1:
                output = spoken_form = row[0]
            else:
                if is_spoken_form_first:
                    spoken_form, output = row[:2]
                else:
                    output, spoken_form = row[:2]

                if len(row) > 2:
                    print(
                        f'"{f.name}": More than two values in row: {row}.'
                        + " Ignoring the extras."
                    )
            # Leading/trailing whitespace in spoken form can prevent recognition.
            spoken_form = spoken_form.strip()
            mapping[spoken_form] = output

    return mapping


def write_csv_defaults(
    path: Path,
    headers: tuple[str, str],
    default: dict[str, str] = None,
    is_spoken_form_first: bool = False,
) -> None:
    if not path.is_file() and default is not None:
        with open(path, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for key, value in default.items():
                if key == value:
                    writer.writerow([key])
                elif is_spoken_form_first:
                    writer.writerow([key, value])
                else:
                    writer.writerow([value, key])


def track_csv_list(
    filename: str,
    headers: tuple[str, str],
    default: dict[str, str] = None,
    is_spoken_form_first: bool = False,
) -> DecoratorT:
    assert filename.endswith(".csv")
    path = SETTINGS_DIR / filename
    write_csv_defaults(path, headers, default, is_spoken_form_first)

    def decorator(fn: CallbackT) -> CallbackT:
        @resource.watch(str(path))
        def on_update(f):
            data = read_csv_list(f, headers, is_spoken_form_first)
            fn(data)

    return decorator


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
