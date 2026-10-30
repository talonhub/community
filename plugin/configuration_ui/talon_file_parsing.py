import re
from ast import literal_eval
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SettingFileSettingInformation:
    """Information on a setting assignment in a .talon file"""

    value: Any
    start_line_index: int
    line_after_index: int
    is_activated: bool = True
    # indentation before the assignment including the # if it is commented
    assignment_prefix: str = ""


# used for no value available. None is valid in TalonScript, so use this instead
VALUE_UNAVAILABLE = ...
# matches commented and uncommented tag activations. Parses the name of the tag.
TAG_PREFIX_PATTERN = re.compile(r"^#?\s*tag\(\):\s*(?P<name>.+)")
# matches commented and uncommented setting assignments. Parses the prefix before the assignment including spaces and hash signs, the setting name, and the value assigned to the setting.
SETTING_ASSIGNMENT_PATTERN = re.compile(
    r"^(?P<assignment_prefix>[\s|#]+)(?P<name>\w\S*)\s*=\s*(?P<value>.+)"
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
    # literal_eval can throw many kinds of exceptions, so this is simpler than handling them explicitly
    except Exception:
        return VALUE_UNAVAILABLE


def _remove_prefix(line: str, prefix):
    """Remove the prefix at the start of a line"""
    if not line.startswith(prefix):
        raise ValueError(f"line ({line}) did not start with prefix ({prefix})")
    if len(line) == prefix:
        return ""
    return line.removeprefix(prefix)


def _parse_multiline_string(lines, assignment_prefix):
    """Convert TalonScript multiline string lines to a Python string. Assumes that every line starts with the assignment prefix, which may not be the case if the string is commented"""
    total_text = "\n".join([_remove_prefix(l, assignment_prefix) for l in lines[1:]])[:-3]
    return _parse_value(f'"""{total_text}"""')


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

    def _parse_multiline_string(self, value_text, assignment_prefix, i):
        """Parses the multiline string starting at line with index i with value_text containing the starting characters. Assume that each line of the string starts with assignment prefix and give up otherwise. Return the multiline string and its last line index"""
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
                        assignment_prefix,
                    )
                break
            i += 1
        return value, i

    def _parse_file(self, path: Path):
        """Parse the .talon file at path for relevant information"""
        self.lines = path.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            if match := TAG_PREFIX_PATTERN.fullmatch(line):
                name = match.group("name").strip()
                is_active = not line.startswith("#")
                information = SettingFileSettingInformation(is_active, i, i + 1)
                self._add_information(name, information, self.tags, self.duplicate_tags)
            elif match := SETTING_ASSIGNMENT_PATTERN.fullmatch(line):
                assignment_prefix, name, value_text = match.groups()
                is_active = "#" not in assignment_prefix
                starting_index = i
                if _is_start_of_multiline_string(value_text):
                    value, i = self._parse_multiline_string(
                        value_text, assignment_prefix, i
                    )
                else:
                    value = _parse_value(value_text.strip())
                information = SettingFileSettingInformation(
                    value, starting_index, i + 1, is_active, assignment_prefix
                )
                self._add_information(
                    name, information, self.settings, self.duplicate_settings
                )
            i += 1


def parse_settings(path: Path):
    """Compute the tags and settings at the path"""
    parser = SettingsParser(path)
    return parser.tags, parser.settings
