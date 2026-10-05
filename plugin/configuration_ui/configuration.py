from talon import Module, fs, registry

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

from .gui import open_gui

import egui
from ast import literal_eval

@dataclass
class SettingFileSettingInformation:
	value: Any
	description: str
	is_deactivated: bool=False

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

def compute_setting(line: str, prefix: str):
	if not line.startswith(prefix):
		return None
	equals_index = line.find(" = ")
	if equals_index == -1 or equals_index >= len(line) - 3:
		return None
	if len(line) < len(prefix):
		return None
	if not line[len(prefix)].isalpha():
		return None
	value = parse_value(line[equals_index+3:].strip())
	name = line[len(prefix):equals_index]
	return name, value

def parse_value(value):
	if value == "true":
		return True
	elif value == "false":
		return False
	else:
		try:
			return literal_eval(value)
		except Exception as ex:
			return None

SETTING_INDENTATION_PREFIX = "    "

def parse_settings(path):
	tags = {}
	settings = {}
	description = []
	with open(path, "r") as f:
		for l in f.readlines():
			line = l.rstrip("\n\r")
			if tag := compute_commented_tag(line):
				tags[tag] = SettingFileSettingInformation(False, "\n".join(description))
				description.clear()
			elif setting := compute_setting(line, COMMENTED_SETTING_PREFIX):
				name, value = setting
				settings[name] = SettingFileSettingInformation(value, "\n".join(description), is_deactivated=True)
				description.clear()
			elif setting := compute_setting(line, SETTING_INDENTATION_PREFIX):
				name, value = setting
				settings[name] = SettingFileSettingInformation(value, "\n".join(description))
				description.clear()
			elif tag := compute_tag(line):
				tags[tag] = SettingFileSettingInformation(True, "\n".join(description))
				description.clear()
			elif line.lstrip().startswith("# "):
				comment = line.strip()[1:].strip()
				description.append(comment)
			else:
				description.clear()
	return tags, settings

def convert_value_to_talon_script_literal(value) -> str:
	if isinstance(value, bool):
		return str(value).lower()
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, str):
		return f"\"{value.replace('"', '\\"')}\""

def replace_setting_assignment(path, setting_name, new_text):
	current_text = ""
	with open(path, "r") as f:
		current_text = f.read()
	lines = current_text.split("\n")
	setting_text = f"    {setting_name} = "
	commented_setting_text = f"    # {setting_name} = "
	found_setting = False
	for i, line in enumerate(lines):
		if line.startswith(setting_text) or line.startswith(commented_setting_text):
			if found_setting:
				raise IOError(f"Found duplicate setting assignment for {setting_name} inside file {path}")
			lines[i] = new_text
			found_setting = True
	if not found_setting:
		raise IOError(f"Could not find {setting_name} inside file {path}")
	with open(path, "w") as f:
		f.write("\n".join(lines))

def update_setting(path, setting_name, new_value):
	"""Updates the file to set the setting to a new value.
		Assumes that the setting takes a single line and that there is no variable name getting created equalling the setting name
		"""
	converted_value = convert_value_to_talon_script_literal(new_value)
	new_setting_text = f"    {setting_name} = {converted_value}"
	replace_setting_assignment(path, setting_name, new_setting_text)

def update_tag(path, name, should_be_active):
	lines = []
	with open(path, "r") as f:
		lines = [l for l in f.readlines()]
	if not lines:
		raise IOError(f"Found no lines in the file {path}!")
	matching_line = None
	is_active = None
	active_string = f"tag(): {name}"
	deactivated_string = f"# tag(): {name}"
	for i, line in enumerate(lines):
		stripped_line = line.rstrip()
		encountered_duplicate = False
		if stripped_line == deactivated_string:
			if matching_line is not None:
				encountered_duplicate = True
			else:
				matching_line = i
				is_active = False
		elif stripped_line == active_string:
			if matching_line is not None:
				encountered_duplicate = True
			else:
				matching_line = i
				is_active = True
		if encountered_duplicate:
			raise IOError(f"Encountered the tag {name} twice in the file {path}!")
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
		
def compute_vertical_size_from_number_of_lines_in_description(setting: Setting, ui):
	number_of_description_lines = len(setting.description.split("\n"))
	row_size = ui.spacing().item_spacing.y + egui.TextStyle.Body.resolve(ui.style()).size
	interactive_size = ui.spacing().item_spacing.y + ui.spacing().interact_size.y
	return interactive_size + row_size*number_of_description_lines

SETTINGS_PATH = Path(__file__).parent.parent.parent / "settings.talon"
MODE_INDICATOR_PATH = Path(__file__).parent.parent / "mode_indicator" / "mode_indicator.talon"
SUBTITLES_PATH = Path(__file__).parent.parent / "subtitles" / "subtitles.talon"
RELEVANT_PATHS = [SETTINGS_PATH, MODE_INDICATOR_PATH, SUBTITLES_PATH]

DEFAULT_DESCRIPTION = "Something went wrong. Could not find the setting description."

@dataclass
class Setting:
	name: str
	draw: Callable
	update_function: Callable=update_setting
	path: Path=SETTINGS_PATH
	is_tag: bool=False
	is_deactivated: bool=False
	value: Any=None
	compute_vertical_size: Callable=compute_vertical_size_from_number_of_lines_in_description
	draws_description: bool=False
	
	def get_description(self):
		try:
			if self.is_tag:
				return registry.decls.tags[self.name].desc
			else:
				return registry.decls.settings[self.name].desc
		except Exception as ex:
			return DEFAULT_DESCRIPTION


async def draw_setting_un_commenting_button(ui, setting: Setting):
	file_name = setting.path.stem + setting.path.suffix
	if ui.button(f"Click this if you want to set {setting.name} in {file_name}").clicked():
		update_setting(setting.path, setting.name, setting.value.get())

async def draw_toggle(setting: Setting, ui):
	value = setting.value.get()
	ui.checkbox(setting.value, setting.get_description())
	new_value = setting.value.get()
	if value != new_value:
		setting.update_function(setting.path, setting.name, new_value)
		
def create_tag_setting(name):
	return Setting(
		name,
		draw_toggle,
		update_tag,
		is_tag=True,
		draws_description=True,
	)

def create_boolean_setting(name, path=None):
	result = Setting(
		name,
		draw_toggle,
		update_setting,
		draws_description=True,
	)
	if path is not None:
		result.path = path
	return result

async def draw_numeric_input(setting: Setting, ui, minimum, maximum):
	old_value = setting.value.get()
	ui.add(egui.DragValue(setting.value))
	value = setting.value.get()
	if minimum is not None and value < minimum:
		setting.value.set(minimum)
	if maximum is not None and value > maximum:
		setting.value.set(maximum)
	if old_value != value:
		setting.update_function(setting.path, setting.name, value)

async def draw_slider_input(setting: Setting, ui, minimum, maximum):
	old_value = setting.value.get()
	slider = egui.Slider(
		setting.value,
		minimum,
		maximum)
	ui.add(slider)
	value = setting.value.get()
	if old_value != value:
		setting.update_function(setting.path, setting.name, value)

async def draw_single_line_text_input(setting: Setting, ui):
	old_value = setting.value.get()
	ui.add(egui.TextEdit.singleline(setting.value))
	value = setting.value.get()
	if old_value != value:
		setting.update_function(setting.path, setting.name, value)

def create_numeric_setting(name, minimum=None, maximum=None, path=None, use_slider=False):
	ui_function = draw_slider_input if use_slider else draw_numeric_input
	result = Setting(
		name,
		lambda setting, ui: ui_function(setting, ui, minimum, maximum),
	)
	if path is not None:
		result.path = path
	return result

def create_single_line_text_setting(name, path=None):
	result = Setting(
		name,
		draw_single_line_text_input,
	)
	if path is not None:
		result.path = path
	return result

@dataclass
class Page:
	title: str
	description: str
	settings: list[Setting]
	prefix: str=""

def update_setting_information(setting: Setting, file_setting_information: SettingFileSettingInformation):
	setting.value = egui.Mutable(file_setting_information.value)
	setting.is_deactivated = file_setting_information.is_deactivated

def compute_readable_name(setting_name, page_prefix: str):
	words = []
	if page_prefix and page_prefix in setting_name:
		name = setting_name[len(page_prefix):]
	else:
		prefix, name = setting_name.split(".")
		if prefix != "user":
			words.append(prefix)
	words.extend(name.split("_"))
	capitalized_words = [w.capitalize() for w in words]
	return " ".join(capitalized_words)

class Manager:
	def __init__(self):
		pages = [
			Page(
				"Text Insertion",
				"",
				[
					create_tag_setting("user.unprefixed_numbers"),
					create_numeric_setting("user.paste_to_insert_threshold", -1),
					create_boolean_setting("user.context_sensitive_dictation"),
					create_numeric_setting("user.insert_between_wait", 0),
				]
			),
			Page(
				"Speech Recognition",
				"",
				[
					create_numeric_setting("speech.timeout", 0.0),
					create_single_line_text_setting("user.initial_mode"),
					create_numeric_setting("user.listening_timeout_minutes", -1),
				]
			),
			Page(
				"Scrolling",
				"",
				[
					create_numeric_setting("user.mouse_continuous_scroll_amount", 1),
					create_numeric_setting("user.mouse_gaze_scroll_speed_multiplier", 1.0),
					create_numeric_setting("user.mouse_continuous_scroll_acceleration", 1),
					create_boolean_setting("user.mouse_enable_pop_stops_scroll"),
					create_boolean_setting("user.mouse_enable_hiss_scroll"),
					create_numeric_setting("user.hiss_scroll_debounce_time", 0),
					create_boolean_setting("user.mouse_hide_mouse_gui"),
					create_numeric_setting("user.mouse_wheel_down_amount", 0),
					create_numeric_setting("user.mouse_wheel_horizontal_amount", 0)
				]
			),
			Page(
				"Mouse Grid",
				"",
				[
					create_boolean_setting("user.grids_put_one_bottom_left"),
					create_boolean_setting("user.grid_show_zoomed"),
				]
			),
			Page(
				"Command History",
				"",
				[
					create_numeric_setting("user.command_history_display", 1),
					create_numeric_setting("user.command_history_size", 1),
				]
			),
			Page(
				"Popping",
				"Decide what should happen when you make a popping noise",
				[
					create_tag_setting("user.pop_twice_to_repeat"),
					create_tag_setting("user.pop_twice_to_wake"),
					create_numeric_setting("user.double_pop_speed_minimum", 0.0),
					create_numeric_setting("user.double_pop_speed_maximum", 0.0),
					create_numeric_setting("user.mouse_enable_pop_click", 0, 2),
					create_boolean_setting("user.mouse_enable_pop_stops_scroll"),
					create_boolean_setting("user.mouse_enable_pop_stops_drag"),
				]
			),
			Page(
				"Help System",
				"",
				[
					create_numeric_setting("user.help_max_command_lines_per_page", 1),
					create_numeric_setting("user.help_max_contexts_per_page", 1),
					create_boolean_setting("user.help_sort_contexts_by_specificity"),
				]
			),
			Page(
				"Window Management",
				"",
				[
					create_single_line_text_setting("user.window_snap_screen"),
					create_tag_setting("user.experimental_window_layout"),
				]
			),
			Page(
				"Mode Indicator",
				"The mode indicator shows a colored circle indicating which mode is active.",
				[
					create_boolean_setting("user.mode_indicator_show", MODE_INDICATOR_PATH),
					create_boolean_setting("user.mode_indicator_show_microphone_name", MODE_INDICATOR_PATH),
					create_numeric_setting("user.mode_indicator_size", 1, path=MODE_INDICATOR_PATH),
					create_numeric_setting("user.mode_indicator_x", 0.0, 1.0, MODE_INDICATOR_PATH, use_slider=True),
					create_numeric_setting("user.mode_indicator_y", 0.0, 1.0, MODE_INDICATOR_PATH, use_slider=True),
					create_numeric_setting("user.mode_indicator_color_alpha", 0.0, 1.0, MODE_INDICATOR_PATH, use_slider=True),
					create_numeric_setting("user.mode_indicator_color_gradient", 0.0, 1.0, MODE_INDICATOR_PATH, use_slider=True),
					create_single_line_text_setting("user.mode_indicator_color_text", MODE_INDICATOR_PATH),
					create_single_line_text_setting("user.mode_indicator_color_mute", MODE_INDICATOR_PATH),
					create_single_line_text_setting("user.mode_indicator_color_sleep", MODE_INDICATOR_PATH),
					create_single_line_text_setting("user.mode_indicator_color_deep_sleep", MODE_INDICATOR_PATH),
					create_single_line_text_setting("user.mode_indicator_color_dictation", MODE_INDICATOR_PATH),
					create_single_line_text_setting("user.mode_indicator_color_mixed", MODE_INDICATOR_PATH),
					create_single_line_text_setting("user.mode_indicator_color_command", MODE_INDICATOR_PATH),
					create_single_line_text_setting("user.mode_indicator_color_other", MODE_INDICATOR_PATH),
				],
				prefix="user.mode_indicator_"
			),
			Page(
				"Subtitles",
				"Configuration for Community's subtitles (not the Talon builtin subtitles)",
				[
					create_boolean_setting("user.subtitles_show", SUBTITLES_PATH),
					create_single_line_text_setting("user.subtitles_screens", SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_size", 0, path=SUBTITLES_PATH),
					create_single_line_text_setting("user.subtitles_color", SUBTITLES_PATH),
					create_single_line_text_setting("user.subtitles_color_outline", SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_timeout_per_char", 0, path=SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_timeout_min", 0, path=SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_timeout_max", 0, path=SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_y", 0.0, 1.0, path=SUBTITLES_PATH, use_slider=True),
				],
				prefix="user.subtitles_"
			),
			Page(
				"Miscellaneous",
				"",
				[
					create_numeric_setting("user.mouse_click_hold", 0),
					create_boolean_setting("user.file_manager_auto_show_pickers"),
					create_boolean_setting("user.strict_command_deprecation"),
					create_numeric_setting("user.selected_text_timeout", 0.0),
					create_tag_setting("user.mouse_cursor_commands_enable"),
				]
			)
		]
		self.pages = {page.title: page for page in pages}
		self.page = ""
		for path in RELEVANT_PATHS:
			self.on_change(path)

	def on_change(self, path):
		tags, settings = parse_settings(path)
		for page in self.pages.values():
			for setting in page.settings:
				if setting.path != path:
					continue
				name = setting.name
				if setting.is_tag:
					if name in tags:
						tag = tags[name]
						update_setting_information(setting, tag)
				elif name in settings:
					setting_information = settings[name]
					update_setting_information(setting, setting_information)
	
	async def draw(self, ui):
		total_available_height = ui.available_height()
		async with ui.horizontal():
			await self.draw_page_navigation(ui, total_available_height)
			available_width = ui.available_width()
			interaction_region_space = egui.Vec2(available_width, total_available_height)
			async with ui.allocate_ui(interaction_region_space) as interaction_ui, ui.vertical():
				await self.draw_current_page(interaction_ui, total_available_height)

	async def draw_page_navigation(self, ui, total_available_height):
		async with ui.vertical():
			for page in self.pages:
				if ui.selectable_label(page == self.page, page).clicked():
					self.page = page
			ui.add_space(total_available_height - ui.min_size().y)
		ui.separator()

	async def draw_current_page(self, ui, total_available_height):
		if not self.page:
			return
		page = self.pages[self.page]
		# use a single column table with heterogeneous rows later
		async with egui.ScrollArea.vertical().max_height(total_available_height).show():
			ui.strong(page.title)
			if page.description:
				ui.label(page.description)
			ui.separator()
			for setting in page.settings:
				async with ui.group():
					ui.strong(compute_readable_name(setting.name, page.prefix))
					ui.weak(setting.name)
					ui.add_space(5)
					if not setting.draws_description:
						ui.label(setting.get_description())
					if setting.is_deactivated:
						await draw_setting_un_commenting_button(ui, setting)
					else:
						await setting.draw(setting, ui)
				ui.add_space(10)

manager = Manager()

@open_gui(x=0.25, y=0.25, width=0.5, height=0.5, toplevel=False, decorated=True)
async def draw(ui, helpers):
	await manager.draw(ui)

def handle_file_update(path, flags):
	if manager:
		manager.on_change(Path(path))
		draw.refresh()

for path in RELEVANT_PATHS:
	fs.watch(path, handle_file_update)

mod = Module()
@mod.action_class
class Actions:
	def show_configuration_window():
		"""Show the Community configuration window"""
		draw.show()

	def hide_configuration_window():
		"""Hide the Community configuration window"""
		draw.hide()