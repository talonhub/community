import csv
import os
from pathlib import Path

from talon import Module, actions, resource

mod = Module()

DEFAULT_SETTINGS_DIR = Path(__file__).parents[1] / "settings"

# NOTE: Adapted from <https://github.com/cursorless-dev/cursorless/blob/f0db4113dc055aefa4e0f8ccae4f6c6e1349f3da/cursorless-talon/src/csv_overrides.py#L16-L21>
community_settings_directory = mod.setting(
    "community_settings_directory",
    type=str,
    default=str(DEFAULT_SETTINGS_DIR),
    desc="The directory to use for settings csvs relative to talon user directory",
)

# NOTE: Adapted from <https://github.com/cursorless-dev/cursorless/blob/f0db4113dc055aefa4e0f8ccae4f6c6e1349f3da/cursorless-talon/src/csv_overrides.py#L319-L329>
def get_full_path(filename: str):
    if not filename.endswith(".csv"):
        filename = f"{filename}.csv"

    settings_directory = Path(community_settings_directory.get())
    if not settings_directory.exists():
        settings_directory.mkdir(parents=True)

    if not settings_directory.is_absolute():
        user_dir: Path = actions.path.talon_user()
        settings_directory = user_dir / settings_directory

    return (settings_directory / filename).resolve()


def get_list_from_csv(
    filename: str, headers: tuple[str, str], default: dict[str, str] = {}
):
    """Retrieves list from CSV"""
    path = get_full_path(filename)

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
    path = get_full_path(filename)

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
