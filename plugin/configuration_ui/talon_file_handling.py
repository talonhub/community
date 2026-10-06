from dataclasses import dataclass

from ast import literal_eval
import re

SPACES_PER_INDENT = 4
STANDARD_COMMENT_SIZE = SPACES_PER_INDENT + 2
MINIMAL_COMMENT_SIZE = SPACES_PER_INDENT + 1

@dataclass
class SettingFileSettingInformation:
	value: Any
	line_index: int
	is_activated: bool=True

COMMENTED_TAG_PREFIX = "# tag(): "
TAG_PREFIX = "tag(): "
def compute_tag(line):
	if line.startswith(COMMENTED_TAG_PREFIX):
		return line[len(COMMENTED_TAG_PREFIX):].strip(), False
	elif line.startswith(TAG_PREFIX):
		return line[len(TAG_PREFIX):].strip(), True
	return None

INDENTED_COMMENT_PREFIX = "    # "
INDENTED_COMMENT_PREFIX_WITHOUT_SPACE = "    #"

def is_start_of_multiline_string(line):
	return line.endswith('"""') or line.endswith("'''")

def compute_setting(line: str, prefix: str):
	# we are checking for the pattern:
	# prefix at least one letter = something
	if not line.startswith(prefix):
		return None
	lefthand_side, separator, righthand_side = line.partition(" = ")
	name = lefthand_side[len(prefix):]
	
	# give up if the separator is not found, there is no righthand side, or there is no valid name
	if not righthand_side or not name or not name[0].isalpha():
		return None
	is_multiline_string = is_start_of_multiline_string(righthand_side.lstrip())
	if is_multiline_string:
		value = righthand_side.lstrip()
	else:
		value = parse_value(righthand_side.strip())
	return name, value, is_multiline_string

VALUE_UNAVAILABLE = ...

def parse_value(value):
	if value == "true":
		return True
	elif value == "false":
		return False
	else:
		try:
			return literal_eval(value)
		except Exception as ex:
			return VALUE_UNAVAILABLE

def remove_starting_single_indent(line: str, is_commented: bool):
	if is_commented and line.startswith(INDENTED_COMMENT_PREFIX):
		return line[STANDARD_COMMENT_SIZE:]
	elif is_commented and line.startswith(INDENTED_COMMENT_PREFIX_WITHOUT_SPACE):
		return line[MINIMAL_COMMENT_SIZE:]
	return line[SPACES_PER_INDENT:]

def parse_multiline_string(lines, is_commented):
	return "\n".join([remove_starting_single_indent(l, is_commented) for l in lines[1:]])[:-3]

def compute_commented_or_not_commented_setting(line):
	if setting := compute_setting(line, INDENTED_COMMENT_PREFIX):
		return *setting, False
	elif setting := compute_setting(line, INDENTATION):
		return *setting, True
	return None

INDENTATION = "    "

class SettingsParser:
	__slots__ = ('_is_activated', '_multiline_string_lines', 'settings', 'duplicate_tags', 'duplicate_settings', '_multiline_string_starting_characters', 'tags', '_current_name', 'lines')
	def __init__(self, path):
		self.tags = {}
		self.settings = {}
		self.duplicate_tags = set()
		self.duplicate_settings = set()
		self.lines = []

		self._current_name = None
		self._multiline_string_lines = []
		self._is_activated = None
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
		value = parse_multiline_string(self._multiline_string_lines, not self._is_activated)
		self._add_setting(self._current_name, SettingFileSettingInformation(value, line_index - value.count("\n") - 1, self._is_activated))
		self._reset_multiline_state()

	def _reset_multiline_state(self) -> None:
		self._multiline_string_lines = []
		self._current_name = self._is_activated = self._multiline_string_starting_characters = None

	def _process_simple_line(self, line, line_index) -> None:
		if tag := compute_tag(line):
			name, is_active = tag
			self._add_tag(name, is_active, line_index)
		elif setting := compute_commented_or_not_commented_setting(line):
			name, value, is_multiline_start, activated = setting
			if is_multiline_start:
				self._current_name = name
				self._multiline_string_lines = [value]
				self._multiline_string_starting_characters = value[:3]
				self._is_activated = activated
			else:
				self._add_setting(name, SettingFileSettingInformation(value, line_index, is_activated=activated))

	def _parse_file(self, path):
		with open(path, "r", encoding="utf-8") as f:
			self.lines = [l.rstrip("\n\r") for l in f.readlines()]
		for i, line in enumerate(self.lines):
			if self._multiline_string_starting_characters is not None:
				self._add_to_multiline_string(line, i)
			else:
				self._process_simple_line(line, i)

def parse_settings(path):
	parser = SettingsParser(path)
	return parser.tags, parser.settings

def convert_value_to_talon_script_literal(value, is_comment=False) -> str:
	if isinstance(value, bool):
		return str(value).lower()
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, str):
		value = value.replace('"', '\\"')
		if "\n" in value:
			lines = value.split("\n")
			prefix = INDENTED_COMMENT_PREFIX if is_comment else INDENTATION
			indented_lines = [f"{prefix}{l}" for l in lines]
			return f"\"\"\"\n{"\n".join(indented_lines)}\"\"\""
		else:
			return f"\"{value}\""
	raise ValueError(f"Could not convert value {value} to Talonscript")

def replace_setting_assignment(path, setting_name, new_text):
	parser = SettingsParser(path)
	if setting_name in parser.duplicate_settings:
		raise OSError(f"Found duplicate setting assignment for {setting_name} inside file {path}")
	if setting_name not in parser.settings:
		raise OSError(f"Could not find {setting_name} inside file {path}")
	lines = parser.lines
	info = parser.settings[setting_name]
	lines[info.line_index] = new_text
	# remove original multiline string text after the line
	value = info.value
	if isinstance(value, str) and "\n" in value:
		line_after_multiline_string = info.line_index + value.count("\n") + 2
		lines = lines[:info.line_index+1] + lines[line_after_multiline_string:]

	with open(path, "w") as f:
		f.write("\n".join(lines))

def update_setting(path, setting_name, new_value, make_comment=False):
	converted_value = convert_value_to_talon_script_literal(new_value, is_comment=make_comment)
	prefix = INDENTED_COMMENT_PREFIX if make_comment else INDENTATION
	new_setting_text = f"{prefix}{setting_name} = {converted_value}"
	replace_setting_assignment(path, setting_name, new_setting_text)

def toggle_setting_activation(setting):
	try:
		update_setting(setting.path, setting.name, setting.value.get(), make_comment=setting.is_activated)
	except Exception as ex:
		return f"Something went wrong trying to toggle a setting activation: {ex}"

def update_tag(path, name, should_be_active):
	parser = SettingsParser(path)
	if name in parser.duplicate_tags:
		raise OSError(f"Found duplicate tag activation for tag {name} in the file {path}!")
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
		
