import re
from ast import literal_eval
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SettingFileSettingInformation:
    value: Any
    line_index: int
    is_activated: bool = True


INDENTATION = "    "
TAG_PREFIX_PATTERN = re.compile(r"^#?\s*tag\(\):\s*(?P<name>.+)")
INDENTED_COMMENT_PREFIX = "    # "
SETTING_PATTERN = re.compile(
    r"^(?P<indentation>[\s|#]+)(?P<name>\w\S*)\s*=\s*(?P<value>.+)"
)


def _is_start_of_multiline_string(line):
    return line.endswith('"""') or line.endswith("'''")


VALUE_UNAVAILABLE = ...


def _parse_value(value):
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return literal_eval(value)
    except Exception:
        return VALUE_UNAVAILABLE


def _remove_starting_single_indent(line: str, is_commented: bool, indentation):
    if is_commented:
        indentation += "#"
    if len(line) < indentation:
        raise ValueError(
            f"Could not parse multiline string at line {line}, which did not have the expected indentation of size {len(indentation)}!"
        )
    if len(line) == indentation:
        return ""
    return line.removeprefix(indentation)


def _parse_multiline_string(lines, is_commented, indentation):
    return "\n".join(
        [
            _remove_starting_single_indent(l, is_commented, indentation)
            for l in lines[1:]
        ]
    )[:-3]


def _parse_indentation_spaces(indentation):
    number_of_leading_spaces = len(indentation) - len(indentation.lstrip())
    return indentation[:number_of_leading_spaces]


class SettingsParser:
    __slots__ = (
        "_is_activated",
        "_multiline_string_lines",
        "_current_indentation",
        "settings",
        "duplicate_tags",
        "duplicate_settings",
        "_multiline_string_starting_characters",
        "tags",
        "_current_name",
        "lines",
    )

    def __init__(self, path):
        self.tags = {}
        self.settings = {}
        self.duplicate_tags = set()
        self.duplicate_settings = set()
        self.lines = []

        self._current_name = None
        self._multiline_string_lines = []
        self._is_activated = None
        self._current_indentation = None
        self._multiline_string_starting_characters = None
        self._parse_file(path)

    def _is_duplicate(self, name, dictionary, duplicates):
        if name in duplicates:
            return True
        if name in dictionary:
            duplicates.add(name)
            dictionary.pop(name)
            return True
        return False

    def _add_setting(self, name, information):
        if self._is_duplicate(name, self.settings, self.duplicate_settings):
            return
        self.settings[name] = information

    def _add_tag(self, tag, is_active, line_index):
        if self._is_duplicate(tag, self.tags, self.duplicate_tags):
            return
        self.tags[tag] = SettingFileSettingInformation(is_active, line_index)

    def _add_to_multiline_string(self, line, line_index) -> None:
        if self._multiline_string_starting_characters is not None:
            self._multiline_string_lines.append(line)
            if line.strip().endswith(self._multiline_string_starting_characters):
                self._finalize_multiline(line_index)

    def _finalize_multiline(self, line_index) -> None:
        value = _parse_multiline_string(
            self._multiline_string_lines,
            not self._is_activated,
            self._current_indentation,
        )
        self._add_setting(
            self._current_name,
            SettingFileSettingInformation(
                value, line_index - value.count("\n") - 1, self._is_activated
            ),
        )
        self._reset_multiline_state()

    def _reset_multiline_state(self) -> None:
        self._multiline_string_lines = []
        self._current_indentation = self._current_name = self._is_activated = (
            self._multiline_string_starting_characters
        ) = None

    def _process_simple_line(self, line, line_index) -> None:
        if match := TAG_PREFIX_PATTERN.search(line):
            name = match.group("name").strip()
            is_active = not line.startswith("#")
            self._add_tag(name, is_active, line_index)
        elif match := SETTING_PATTERN.search(line):
            indentation, name, value_text = match.groups()
            is_multiline_start = _is_start_of_multiline_string(value_text)
            is_active = "#" not in indentation
            if is_multiline_start:
                self._current_name = name
                self._multiline_string_lines = [value_text]
                self._multiline_string_starting_characters = value_text[:3]
                self._is_activated = is_active
                self._current_indentation = _parse_indentation_spaces(indentation)
            else:
                value = _parse_value(value_text.strip())
                self._add_setting(
                    name,
                    SettingFileSettingInformation(
                        value, line_index, is_activated=is_active
                    ),
                )

    def _parse_file(self, path: Path):
        self.lines = path.read_text().splitlines()
        for i, line in enumerate(self.lines):
            if self._multiline_string_starting_characters is not None:
                self._add_to_multiline_string(line, i)
            else:
                self._process_simple_line(line, i)


def parse_settings(path):
    parser = SettingsParser(path)
    return parser.tags, parser.settings


def _convert_value_to_talon_script_literal(value, is_comment=False) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        value = value.replace('"', '\\"')
        if "\n" in value:
            lines = value.split("\n")
            prefix = INDENTED_COMMENT_PREFIX if is_comment else INDENTATION
            indented_lines = "\n".join([f"{prefix}{l}" for l in lines])
            return f'"""\n{indented_lines}"""'
        return f'"{value}"'
    raise ValueError(f"Could not convert value {value} to Talonscript")


def _replace_setting_assignment(path, setting_name, new_text):
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
    converted_value = _convert_value_to_talon_script_literal(
        new_value, is_comment=make_comment
    )
    prefix = INDENTED_COMMENT_PREFIX if make_comment else INDENTATION
    new_setting_text = f"{prefix}{setting_name} = {converted_value}"
    _replace_setting_assignment(path, setting_name, new_setting_text)


def toggle_setting_activation(setting):
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
