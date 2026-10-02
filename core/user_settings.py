import csv
from collections.abc import Callable
from pathlib import Path
from typing import IO

from talon import actions, resource, settings

# NOTE: This method requires this module to be one folder below the top-level
#   community folder.
COMMUNITY_ROOT_DIR = Path(__file__).parents[1]

CallbackT = Callable[[dict[str, str]], None]
DecoratorT = Callable[[CallbackT], CallbackT]


def read_csv_list(
    f: IO, headers: tuple[str, str], is_spoken_form_first: bool = False
) -> dict[str, str]:
    rows = read_csv_rows(f, headers)
    mapping = {}
    for row in rows:
        if len(row) == 0:
            # Windows newlines are sometimes read as empty rows.
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


def read_csv_rows(f: IO, headers: tuple[str, ...]) -> list[list[str]]:
    rows = list(csv.reader(f))
    if len(rows) == 0:
        warn_about_error(f"{f.name} is empty!")
    elif len(rows) == 1:
        warn_about_error(f"{f.name} has only the header!")
    if len(rows) >= 1:
        actual_headers = rows[0]
        if actual_headers != list(headers):
            warn_about_error(
                f'"{f.name}": Malformed headers - {actual_headers}.'
                + f" Should be {list(headers)}. Ignoring row."
            )
    if len(rows) < 2:
        return []
    return rows[1:]


def write_csv_defaults(
    path: Path,
    headers: tuple[str, str],
    default: dict[str, str] | None = None,
    is_spoken_form_first: bool = False,
) -> None:
    """Writes a dict of output: spoken form pairs to csv if the file doesn't exist. is_spoken_form_first swaps the order to spoken form: output."""
    rows = []
    for key, value in default.items():
        if key == value:
            rows.append([key])
        elif is_spoken_form_first:
            rows.append([key, value])
        else:
            rows.append([value, key])
    write_csv_default_rows(path, headers, rows)


def write_csv_default_rows(
    path: Path,
    headers: tuple[str, ...],
    default: list[list[str]] | None = None,
) -> None:
    """Writes a list of rows to csv if the file doesn't exist. May be multiple columns"""
    if path.is_file() or default is None:
        return
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(default)


def track_csv_list(
    filename: str,
    headers: tuple[str, str],
    default: dict[str, str] | None = None,
    is_spoken_form_first: bool = False,
    private: bool = False,
) -> DecoratorT:
    assert filename.endswith(".csv")
    path = resolve_setting_file_path(filename, private)
    write_csv_defaults(path, headers, default, is_spoken_form_first)

    def decorator(fn: CallbackT) -> CallbackT:
        @resource.watch(str(path))
        def on_update(f):
            data = read_csv_list(f, headers, is_spoken_form_first)
            fn(data)

    return decorator


def append_to_csv(filename: str, rows: dict[str, str], private: bool = False):
    assert filename.endswith(".csv")
    path = resolve_setting_file_path(filename, private)

    needs_newline = needs_final_newline(path)
    with open(path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if needs_newline:
            writer.writerow([])
        for key, value in rows.items():
            writer.writerow([key] if key == value else [value, key])


def resolve_setting_file_path(filename, private):
    # Make directory on resolve rather than earlier, in case it has been deleted since talon was started
    settings_dir = COMMUNITY_ROOT_DIR / "settings"
    settings_dir.mkdir(exist_ok=True)
    private_dir = COMMUNITY_ROOT_DIR / "private"
    private_dir.mkdir(exist_ok=True)
    return (private_dir / filename) if private else (settings_dir / filename)


def needs_final_newline(path: Path | str) -> bool:
    with open(path) as file:
        line = None
        for line in file:  # noqa: B007
            pass  # iterate through each line in file
    return line is not None and not line.endswith("\n")


WatchCallbackType = Callable[[IO], None]
WatchDecoratorType = Callable[[WatchCallbackType], WatchCallbackType]


def track_file(
    filename: str,
    default: str = "",
    private: bool = False,
) -> WatchDecoratorType:
    path = resolve_setting_file_path(filename, private)
    if not path.is_file():
        path.write_text(default)

    def decorator(fn: WatchCallbackType) -> WatchCallbackType:
        @resource.watch(path)
        def on_update(f):
            fn(f)

        return on_update

    return decorator


RawRowsCallbackT = Callable[[list[list[str]]], None]
RawRowsDecoratorT = Callable[[RawRowsCallbackT], RawRowsCallbackT]


def track_csv_rows(
    filename: str,
    headers: tuple[str, ...],
    default: list[list[str]] | None = None,
    private: bool = False,
) -> RawRowsDecoratorT:
    assert filename.endswith(".csv")
    path = resolve_setting_file_path(filename, private)
    write_csv_default_rows(path, headers, default)

    def decorator(fn: RawRowsCallbackT) -> RawRowsCallbackT:
        @resource.watch(str(path))
        def on_update(f):
            data = read_csv_rows(f, headers)
            fn(data)

        return on_update

    return decorator


def warn_about_error(message: str):
    actions.app.notify(message)
    print(message)


def get_setting_directories(setting) -> list[Path]:
    setting_val = settings.get(setting)
    user_dir = Path(actions.path.talon_user())
    return parse_directories_setting(setting_val, user_dir)


# For inclusion in setting documentation
setting_directory_documentation = """
Accepts a single path, or multiple paths separated by new lines.
Paths must be separated by forward slashs (not the default windows backslash!).
Spaces inside path names are supported directly and do not need to be escaped.
Whitespace around the lines is automatically trimmed.
The `~` character is automatically expanded to the users home directory.
"""


def parse_directories_setting(
    dir_strings: str | None, base_dir: Path | None = None
) -> list[Path]:
    """Parses a newline-separated string of directories into resolved Path objects."""
    if not dir_strings or not dir_strings.strip():
        return []

    dirs: list[Path] = []
    for segment in dir_strings.split("\n"):
        segment = segment.strip()
        if not segment:
            continue

        path = Path(segment).expanduser()
        if not path.is_absolute() and base_dir is not None:
            path = base_dir / path

        dirs.append(path.resolve())

    return dirs
