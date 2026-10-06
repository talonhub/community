from dataclasses import dataclass

from ast import literal_eval

@dataclass
class SettingFileSettingInformation:
	value: Any
	is_activated: bool=True

COMMENTED_TAG_PREFIX = "# tag(): "
TAG_PREFIX = "tag(): "
def compute_commented_tag(line):
	if line.startswith(COMMENTED_TAG_PREFIX):
		return line[len(COMMENTED_TAG_PREFIX):].strip()
	return None

def compute_tag(line):
	if line.startswith(TAG_PREFIX):
		return line[len(TAG_PREFIX):].strip()
	return None

COMMENTED_SETTING_PREFIX = "    # "

def is_start_of_multiline_string(line):
	return line.endswith('"""') or line.endswith("'''")

def compute_setting(line: str, prefix: str):
	if not line.startswith(prefix):
		return None
	equals_index = line.find(" = ")
	# there is no setting here if there is no assignment, there is nothing after the assignment, there is no room for the prefix, and there is no letter right after the prefix
	# we are checking for the pattern:
	# prefix at least one letter = something
	if equals_index == -1 or equals_index >= len(line) - 3 or len(line) < len(prefix) or not line[len(prefix)].isalpha():
		return None
	righthand_side = line[equals_index+3:]
	is_multiline_string = is_start_of_multiline_string(righthand_side.lstrip())
	if is_multiline_string:
		value = righthand_side.lstrip()
	else:
		value = parse_value(righthand_side.strip())
	name = line[len(prefix):equals_index]
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
	if is_commented and line.startswith("    # "):
		return line[6:]
	elif is_commented and line.startswith("    #"):
		return line[5:]
	return line[4:]

def parse_multiline_string(lines, is_commented):
	return "\n".join([remove_starting_single_indent(l, is_commented) for l in lines[1:]])[:-3]

def compute_commented_or_not_commented_setting(line):
	if setting := compute_setting(line, COMMENTED_SETTING_PREFIX):
		return *setting, False
	elif setting := compute_setting(line, SETTING_INDENTATION_PREFIX):
		return *setting, True
	return None

SETTING_INDENTATION_PREFIX = "    "

def parse_settings(path):
	tags = {}
	settings = {}

	# values for keeping track of a setting that has a multiline string value
	current_setting = None
	multiline_string = []
	multiline_string_starting_characters = None
	is_activated = None

	with open(path, "r") as f:
		for l in f.readlines():
			line = l.rstrip("\n\r")
			if multiline_string:
				multiline_string.append(line)
				if line.strip().endswith(multiline_string_starting_characters):
					value = parse_multiline_string(multiline_string, not is_activated)
					settings[current_setting] = SettingFileSettingInformation(value, is_activated)
					current_setting = multiline_string_starting_characters = is_activated = None
					multiline_string.clear()
			elif tag := compute_commented_tag(line):
				tags[tag] = SettingFileSettingInformation(False)
			elif setting := compute_commented_or_not_commented_setting(line):
				name, value, is_multiline_string, activated = setting
				if is_multiline_string:
					current_setting = name
					multiline_string = [value]
					multiline_string_starting_characters = value[:3]
					is_activated = activated
				else:
					settings[name] = SettingFileSettingInformation(value, is_activated=activated)
			elif tag := compute_tag(line):
				tags[tag] = SettingFileSettingInformation(True)
	return tags, settings

def convert_value_to_talon_script_literal(value, is_comment=False) -> str:
	if isinstance(value, bool):
		return str(value).lower()
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, str):
		value = value.replace('"', '\\"')
		if "\n" in value:
			lines = value.split("\n")
			prefix = "    # " if is_comment else "    "
			indented_lines = [f"{prefix}{l}" for l in lines]
			return f"\"\"\"\n{"\n".join(indented_lines)}\"\"\""
		else:
			return f"\"{value}\""
	raise ValueError(f"Could not convert value {value} to Talonscript")

def replace_setting_assignment(path, setting_name, new_text):
	"""Updates the file to set the setting to a new value.
		Assumes that the setting takes a single line and that there is no variable name getting created equalling the setting name
		"""
	current_text = ""
	with open(path, "r") as f:
		current_text = f.read()
	lines = current_text.split("\n")
	setting_text = f"    {setting_name} = "
	commented_setting_text = f"    # {setting_name} = "
	found_setting = False
	# for handling multiline strings
	lines_to_remove = set()
	multiline_string_start = None
	for i, line in enumerate(lines):
		right_stripped_line = line.rstrip()
		if multiline_string_start:
			lines_to_remove.add(i)
			if right_stripped_line.endswith(multiline_string_start):
				multiline_string_start = None
		elif line.startswith(setting_text) or line.startswith(commented_setting_text):
			if found_setting:
				raise OSError(f"Found duplicate setting assignment for {setting_name} inside file {path}")
			lines[i] = new_text
			found_setting = True
			if is_start_of_multiline_string(right_stripped_line):
				multiline_string_start = right_stripped_line[-3:]
	if not found_setting:
		raise OSError(f"Could not find {setting_name} inside file {path}")
	lines = [l for i, l in enumerate(lines) if i not in lines_to_remove]
	with open(path, "w") as f:
		f.write("\n".join(lines))

def update_setting(path, setting_name, new_value):
	converted_value = convert_value_to_talon_script_literal(new_value)
	new_setting_text = f"    {setting_name} = {converted_value}"
	replace_setting_assignment(path, setting_name, new_setting_text)

def comment_out_setting(path, setting_name, new_value):
	converted_value = convert_value_to_talon_script_literal(new_value, is_comment=True)
	new_setting_text = f"    # {setting_name} = {converted_value}"
	replace_setting_assignment(path, setting_name, new_setting_text)

def toggle_setting_activation(setting):
	function = comment_out_setting if setting.is_activated else update_setting
	try:
		function(setting.path, setting.name, setting.value.get())
	except Exception as ex:
		return f"Something went wrong trying to toggle a setting activation: {ex}"

def update_tag(path, name, should_be_active):
	lines = []
	with open(path, "r") as f:
		lines = [l for l in f.readlines()]
	matching_line = None
	is_active = None
	active_string = f"tag(): {name}"
	deactivated_string = f"# tag(): {name}"
	for i, line in enumerate(lines):
		stripped_line = line.rstrip()
		detected_tag_state = None
		if stripped_line == deactivated_string:
			detected_tag_state = False
		elif stripped_line == active_string:
			detected_tag_state = True
		if detected_tag_state is not None:
			if matching_line is not None:
				raise OSError(f"Encountered the tag {name} twice in the file {path}!")
			else:
				matching_line = i
				is_active = detected_tag_state
	if is_active != should_be_active:
		new_string = active_string if should_be_active else deactivated_string
		new_string += "\n"
		if matching_line:
			lines[matching_line] = new_string
		else:
			lines.append("\n")
			lines.append(new_string)
		
		with open(path, "w") as f:
			f.writelines(lines)
		
