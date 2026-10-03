import csv
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import IO

from talon import Module, actions, app, resource, settings

# NOTE: This method requires this module to be one folder below the top-level
#   community folder.
COMMUNITY_ROOT_DIR = Path(__file__).parents[1]

SpokenPairCallbackT = Callable[[dict[str, str]], None]
DecoratorT = Callable[[SpokenPairCallbackT], None]

RawRowsCallbackT = Callable[[list[list[str]]], None]
RawRowsDecoratorT = Callable[[RawRowsCallbackT], RawRowsCallbackT]

mod = Module()


# For inclusion in setting documentation
SETTING_DIRECTORY_DOCUMENTATION = """
Accepts a single path, or multiple paths separated by new lines.
Paths must be separated by forward slashs (not the default Windows backslash!).
Spaces inside path names are supported directly and do not need to be escaped.
Whitespace around the lines is automatically trimmed.
The `~` character is automatically expanded to the users home directory.
"""

mod.setting(
    "extra_settings_dirs",
    type=str,
    default=None,
    desc=f"""
    Additional directories to search for settings .csvs in. Can be relative to the Talon user folder, or absolute.
    The contents of any default tracked csvs will be created unpopulated in all of the specified directories (if they don't already exist) then merged with existing settings lists.
    Useful for storing per machine or per project words to replace, contacts, or file extensions, for example

    {SETTING_DIRECTORY_DOCUMENTATION}
    """,
)


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


def get_setting_directories(setting) -> list[Path]:
    setting_val = settings.get(setting)
    user_dir = Path(actions.path.talon_user())
    return parse_directories_setting(setting_val, user_dir)


@dataclass
class RegisteredCsv:
    headers: tuple[str, str]
    default: dict[str, str] | None
    is_spoken_form_first: bool
    private: bool
    callback_fn: SpokenPairCallbackT


# Keep track of CSV files tracked by register_customization_csv
_registered_csvs: dict[str, RegisteredCsv] = {}


def register_customization_csv(
    filename: str,
    headers: tuple[str, str],
    default: dict[str, str] | None = None,
    is_spoken_form_first: bool = False,
    private: bool = False,
) -> DecoratorT:
    """
    Register a csv within the settings directories for automatic creation and reloading
    """
    assert str(filename).endswith(".csv")

    def decorator(fn: SpokenPairCallbackT) -> None:
        if filename not in _registered_csvs:
            _registered_csvs[filename] = RegisteredCsv(
                headers, default, is_spoken_form_first, private, callback_fn=fn
            )

    return decorator


def apply_registered_csv_on_ready():
    """Once talon is ready and all talon user settings are in place"""
    for filename, entry in _registered_csvs.items():
        core_path, paths = get_settings_csv_paths(filename, entry.private)
        for path in paths:
            path.parent.mkdir(exist_ok=True)

            if path == core_path:
                write_csv_defaults(
                    path,
                    entry.headers,
                    entry.default,
                    entry.is_spoken_form_first,
                )
            else:
                write_csv_defaults(
                    path,
                    entry.headers,
                    is_spoken_form_first=entry.is_spoken_form_first,
                )

            reload_on_change(path, filename)
    app.unregister("ready", apply_registered_csv_on_ready)


app.register("ready", apply_registered_csv_on_ready)


def get_settings_csv_paths(filename: str, private=False):
    # Path for the file version that exists within communities settings folder and is always created
    core_path = resolve_setting_file_path(filename, private)

    # Join with any other settings directories the user may have set
    user_extra_directories = get_setting_directories("user.extra_settings_dirs")
    paths = [core_path] + [dir / filename for dir in user_extra_directories]
    return core_path, paths


def reload_on_change(path: Path, setting_csv_filename: str):
    @resource.watch(str(path))
    def on_update(_):
        load_settings_values(setting_csv_filename)


def load_settings_values(setting_csv_filename):
    try:
        entry = _registered_csvs[setting_csv_filename]
    except KeyError:
        # Shouldn't ever happen, because to get here you should have been registered, but if it does let's not crash.
        return
    core_path, paths = get_settings_csv_paths(setting_csv_filename, entry.private)
    data = {}
    paths = [p for p in paths if p.exists()]
    for path in paths:
        with open(path, encoding="utf-8") as f:
            settings_values = read_csv_list(
                # This watcher callback receives the io for the changed file, but we want to reload all files that provide data for this setting
                f,
                entry.headers,
                entry.is_spoken_form_first,
                permit_no_entries=path != core_path,
            )
            data.update(settings_values)
    entry.callback_fn(data)


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


def read_csv_list(
    f: IO,
    headers: tuple[str, str],
    is_spoken_form_first: bool = False,
    permit_no_entries=False,
) -> dict[str, str]:
    rows = read_csv_rows(f, headers, permit_no_entries)
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


def read_csv_rows(
    f: IO, headers: tuple[str, ...], permit_no_entries=False
) -> list[list[str]]:
    rows = list(csv.reader(f))
    if len(rows) == 0:
        warn_about_error(f"{f.name} is empty!")
    elif len(rows) == 1 and not permit_no_entries:
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
    if default is None:
        default = {}
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


def resolve_setting_file_path(filename: Path | str, private: bool):
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


def warn_about_error(message: str):
    actions.app.notify(message)
    print(message)
