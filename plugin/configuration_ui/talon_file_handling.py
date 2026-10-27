import re
from ast import literal_eval
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SettingFileSettingInformation:
    value: Any
    line_index: int
    is_activated: bool = True


VALUE_UNAVAILABLE = ...
OUTPUT_INDENTATION = "    "
TAG_PREFIX_PATTERN = re.compile(r"^#?\s*tag\(\):\s*(?P<name>.+)")
INDENTED_COMMENT_PREFIX = "    # "
SETTING_ASSIGNMENT_PATTERN = re.compile(
    r"^(?P<indentation>[\s|#]+)(?P<name>\w\S*)\s*=\s*(?P<value>.+)"
)


def _is_start_of_multiline_string(line):
    """Determines if the line contains the start of a multiline string"""
    return line.endswith('"""') or line.endswith("'''")


def _parse_value(value):
    """Convert a TalonScript value to a Python value"""
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return literal_eval(value)
    except Exception:
        return VALUE_UNAVAILABLE


def _remove_starting_single_indent(line: str, indentation):
    """Remove the indentation at the start of a line"""
    if not line.startswith(indentation):
        raise ValueError(
            f"line ({line}) did not start with indentation ({indentation})"
        )
    if len(line) == indentation:
        return ""
    return line.removeprefix(indentation)


def _parse_multiline_string(lines, indentation):
    """Convert TalonScript multiline string lines to a Python string. Assumes that the indentation is the same for every line, which may not be the case if the string is commented"""
    return "\n".join(
        [_remove_starting_single_indent(l, indentation) for l in lines[1:]]
    )[:-3]


class SettingsParser:
    """Identifies the settings and tags in .talon file"""

    __slots__ = (
        "settings",
        "duplicate_tags",
        "duplicate_settings",
        "tags",
        "lines",
    )

    def __init__(self, path):
        self.tags = {}
        self.settings = {}
        self.duplicate_tags = set()
        self.duplicate_settings = set()
        self.lines = []
        self._parse_file(path)

    def _add_information(self, name, information, dictionary, duplicates):
        """Handle the information on the tag or setting. Keep the information if it is new and remember that it is a duplicate otherwise"""
        if name not in duplicates and name not in dictionary:
            dictionary[name] = information
        elif name in dictionary:
            duplicates.add(name)
            dictionary.pop(name)

    def _parse_multiline_string(self, value_text, indentation, i):
        """Parses the multiline string starting at line with index i with value_text containing the starting characters. Assume that each line of the string starts with indentation and give up otherwise. Return the multiline string and its last line index"""
        multiline_string_lines = [value_text]
        multiline_string_starting_characters = value_text[:3]
        value = VALUE_UNAVAILABLE
        i += 1
        while i < len(self.lines):
            line = self.lines[i]
            multiline_string_lines.append(line)
            if line.strip().endswith(multiline_string_starting_characters):
                with suppress(ValueError):
                    value = _parse_multiline_string(
                        multiline_string_lines,
                        indentation,
                    )
                break
            i += 1
        return value, i

    def _parse_file(self, path: Path):
        """Parse the .talon file at path for relevant information"""
        self.lines = path.read_text().splitlines()
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            if match := TAG_PREFIX_PATTERN.search(line):
                name = match.group("name").strip()
                is_active = not line.startswith("#")
                information = SettingFileSettingInformation(is_active, i)
                self._add_information(name, information, self.tags, self.duplicate_tags)
            elif match := SETTING_ASSIGNMENT_PATTERN.search(line):
                indentation, name, value_text = match.groups()
                is_active = "#" not in indentation
                starting_index = i
                if _is_start_of_multiline_string(value_text):
                    value, i = self._parse_multiline_string(value_text, indentation, i)
                else:
                    value = _parse_value(value_text.strip())
                information = SettingFileSettingInformation(
                    value, starting_index, is_active
                )
                self._add_information(
                    name, information, self.settings, self.duplicate_settings
                )
            i += 1


def parse_settings(path: Path):
    """Compute the tags and settings at the path"""
    parser = SettingsParser(path)
    return parser.tags, parser.settings


def _convert_value_to_talon_script_literal(value, is_comment=False) -> str:
    """Convert the Python value to TalonScript"""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        value = value.replace('"', '\\"')
        if "\n" in value:
            lines = value.split("\n")
            prefix = INDENTED_COMMENT_PREFIX if is_comment else OUTPUT_INDENTATION
            indented_lines = "\n".join([f"{prefix}{l}" for l in lines])
            return f'"""\n{indented_lines}"""'
        return f'"{value}"'
    raise ValueError(f"Could not convert value {value} to Talonscript")


def _replace_setting_assignment(path, setting_name, new_text):
    """Update the setting assignment of the setting with given name at the specified path with the new text"""
    parser = SettingsParser(path)
    if setting_name in parser.duplicate_settings:
        raise OSError(
            f"Found duplicate setting assignment for {setting_name} inside file {path}"
        )
    if setting_name not in parser.settings:
        raise OSError(f"Could not find {setting_name} inside file {path}")
    lines = parser.lines
    info = parser.settings[setting_name]
    lines[info.line_index] = new_text
    # remove original multiline string text after the line
    value = info.value
    if isinstance(value, str) and "\n" in value:
        line_after_multiline_string = info.line_index + value.count("\n") + 2
        lines = lines[: info.line_index + 1] + lines[line_after_multiline_string:]

    with open(path, "w") as f:
        f.write("\n".join(lines))


def update_setting(path, setting_name, new_value, make_comment=False):
    """Update the setting assignment of the setting with the given name at the specified path with the new value optionally making it commented"""
    converted_value = _convert_value_to_talon_script_literal(
        new_value, is_comment=make_comment
    )
    prefix = INDENTED_COMMENT_PREFIX if make_comment else OUTPUT_INDENTATION
    new_setting_text = f"{prefix}{setting_name} = {converted_value}"
    _replace_setting_assignment(path, setting_name, new_setting_text)


def toggle_setting_activation(setting):
    """Toggle if the setting is commented"""
    try:
        update_setting(
            setting.path,
            setting.name,
            setting.value.get(),
            make_comment=setting.is_activated,
        )
    except Exception as ex:
        return f"Something went wrong trying to toggle a setting activation: {ex}"


def update_tag(path, name, should_be_active):
    """Update the status of the tag with given name in the file at the path"""
    parser = SettingsParser(path)
    if name in parser.duplicate_tags:
        raise OSError(
            f"Found duplicate tag activation for tag {name} in the file {path}!"
        )
    if name in parser.tags and parser.tags[name].value == should_be_active:
        return

    lines = parser.lines
    prefix = "" if should_be_active else "# "
    new_string = f"{prefix}tag(): {name}"

    if name in parser.tags:
        info = parser.tags[name]
        lines[info.line_index] = new_string
    else:
        lines.append("\n")
        lines.append(new_string)

    with open(path, "w") as f:
        f.write("\n".join(lines))
