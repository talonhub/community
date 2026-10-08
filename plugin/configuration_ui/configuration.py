from talon import Module, fs, registry

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .gui import open_gui

import egui

from .talon_file_handling import *

def compute_vertical_size_from_number_of_lines_in_description(setting: Setting, ui):
	# this function is currently out of date
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
	is_activated: bool=True
	value: egui.Mutable = egui.Mutable(VALUE_UNAVAILABLE)
	compute_vertical_size: Callable=compute_vertical_size_from_number_of_lines_in_description
	draws_description: bool=False
	
	def get_description(self):
		try:
			if self.is_tag:
				description = registry.decls.tags[self.name].desc
			else:
				description = registry.decls.settings[self.name].desc
			if not description:
				return DEFAULT_DESCRIPTION
			return description
		except Exception as ex:
			return DEFAULT_DESCRIPTION


async def draw_toggle(setting: Setting, ui):
	ui.checkbox(setting.value, setting.get_description())
		
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

def make_value_float_if_there_is_a_float_bound(value, minimum, maximum):
	if (isinstance(minimum, float) or isinstance(maximum, float)) and isinstance(value.get(), int):
		value.set(float(value.get()))

async def draw_numeric_input(setting: Setting, ui, minimum, maximum):
	make_value_float_if_there_is_a_float_bound(setting.value, minimum, maximum)
	ui.add(egui.DragValue(setting.value))
	value = setting.value.get()
	if minimum is not None and value < minimum:
		setting.value.set(minimum)
	if maximum is not None and value > maximum:
		setting.value.set(maximum)

async def draw_slider_input(setting: Setting, ui, minimum, maximum):
	make_value_float_if_there_is_a_float_bound(setting.value, minimum, maximum)
	slider = egui.Slider(
		setting.value,
		minimum,
		maximum)
	ui.add(slider)

async def draw_single_line_text_input(setting: Setting, ui):
	ui.add(egui.TextEdit.singleline(setting.value))

async def draw_multiline_text_input(setting: Setting, ui):
	ui.add(egui.TextEdit.multiline(setting.value))

def create_numeric_setting(name, minimum=None, maximum=None, path=None, use_slider=False):
	ui_function = draw_slider_input if use_slider else draw_numeric_input
	result = Setting(
		name,
		lambda setting, ui: ui_function(setting, ui, minimum, maximum),
	)
	if path is not None:
		result.path = path
	return result

def create_text_setting(name, path=None, is_multiline=False):
	ui_function = draw_multiline_text_input if is_multiline else draw_single_line_text_input
	result = Setting(
		name,
		ui_function,
	)
	if path is not None:
		result.path = path
	return result

def hexadecimal_digit_to_decimal(digit):
	if digit.isdigit():
		return int(digit)
	return ord(digit.lower()) - ord("a") + 10

def parse_rgb_from_string(color):
	result = []
	for i in range(0, len(color), 2):
		value = hexadecimal_digit_to_decimal(color[i])*16 + hexadecimal_digit_to_decimal(color[i+1])
		result.append(value)
	return result

def convert_number_to_hexadecimal_digit(number: int):
	if number < 10:
		return str(number)
	return chr(number - 10 + ord("a"))

def convert_number_to_hexadecimal_string(number: int) -> str:
	"""Assumes the number is between 0 and 255"""
	last_place = number % 16
	first_place = number//16
	return f"{convert_number_to_hexadecimal_digit(first_place)}{convert_number_to_hexadecimal_digit(last_place)}"

def convert_rgb_to_string(rgb):
	hexadecimal_digits = [convert_number_to_hexadecimal_string(round(n)) for n in rgb]
	return "".join(hexadecimal_digits)

def is_valid_hexadecimal_digit(c):
	if c.isdigit():
		return True
	if not c.isalpha():
		return False
	character_number = ord(c.lower())
	return character_number >= ord("a") and character_number <= ord("f")

def is_valid_hexadecimal_rgb(text):
	return len(text) == 6 and \
		all([is_valid_hexadecimal_digit(c) for c in text])

async def draw_color_picker_input(setting: Setting, ui):
	value = setting.value.get()
	async with ui.horizontal_wrapped():
		if is_valid_hexadecimal_rgb(value):
			red, green, blue = parse_rgb_from_string(value)
			rgba = egui.Rgba.from_srgba_unmultiplied(red, green, blue, 255)
			rgb = egui.Mutable([rgba.r, rgba.g, rgba.b])
			egui.color_edit_button_rgb(ui, rgb)
			out_rgba = egui.Rgba.from_rgb(*rgb.get())
			new_value = convert_rgb_to_string(out_rgba.to_srgba_unmultiplied()[:3])
			if new_value != setting.value.get().lower():
				setting.value.set(new_value)
		else:
			ui.label("Not valid color.")
		ui.add(egui.TextEdit.singleline(setting.value))


def create_color_picker_setting(name, path=None):
	result = Setting(
		name,
		draw_color_picker_input,
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
	setting.is_activated = file_setting_information.is_activated

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
					create_text_setting("user.initial_mode"),
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
					create_text_setting("user.window_snap_screen"),
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
					create_color_picker_setting("user.mode_indicator_color_text", MODE_INDICATOR_PATH),
					create_color_picker_setting("user.mode_indicator_color_mute", MODE_INDICATOR_PATH),
					create_color_picker_setting("user.mode_indicator_color_sleep", MODE_INDICATOR_PATH),
					create_color_picker_setting("user.mode_indicator_color_deep_sleep", MODE_INDICATOR_PATH),
					create_color_picker_setting("user.mode_indicator_color_dictation", MODE_INDICATOR_PATH),
					create_color_picker_setting("user.mode_indicator_color_mixed", MODE_INDICATOR_PATH),
					create_color_picker_setting("user.mode_indicator_color_command", MODE_INDICATOR_PATH),
					create_color_picker_setting("user.mode_indicator_color_other", MODE_INDICATOR_PATH),
				],
				prefix="user.mode_indicator_"
			),
			Page(
				"Subtitles",
				"Configuration for Community's subtitles (not the Talon builtin subtitles)",
				[
					create_boolean_setting("user.subtitles_show", SUBTITLES_PATH),
					create_text_setting("user.subtitles_screens", SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_size", 0, path=SUBTITLES_PATH),
					create_text_setting("user.subtitles_color", SUBTITLES_PATH),
					create_text_setting("user.subtitles_color_outline", SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_timeout_per_char", 0, path=SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_timeout_min", 0, path=SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_timeout_max", 0, path=SUBTITLES_PATH),
					create_numeric_setting("user.subtitles_y", 0.0, 1.0, path=SUBTITLES_PATH, use_slider=True),
				],
				prefix="user.subtitles_"
			),
			Page(
				"Snippets",
				"",
				[
					create_numeric_setting("user.snippet_raw_text_spaces_per_tab", 0),
					create_text_setting("user.snippets_dir", is_multiline=True),
				]
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
		self.error_message = ""

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
				else:
					if name in settings:
						setting_information = settings[name]
						update_setting_information(setting, setting_information)
					else:
						setting.value.set(VALUE_UNAVAILABLE)

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

	async def draw_setting_ui(self, ui, setting, page):
		old_value = setting.value.get()
		async with ui.group():
			readable_name = compute_readable_name(setting.name, page.prefix)
			async with ui.horizontal():
				if not setting.is_tag:
					if ui.checkbox(egui.Mutable(setting.is_activated), "").clicked():
						error_message = toggle_setting_activation(setting)
						if error_message is not None:
							self.error_message = error_message
				async with ui.vertical():
					ui.strong(readable_name)
					ui.weak(setting.name)
					ui.add_space(5)
					if not setting.draws_description:
						ui.label(setting.get_description())
					if not setting.is_tag and setting.value.get() == VALUE_UNAVAILABLE:
						ui.label("Something went wrong. The setting could not be found or could not be parsed.")
						return 
					async with ui.add_enabled_ui(setting.is_activated or setting.is_tag):
						try:
							await setting.draw(setting, ui)
							value = setting.value.get()
							if old_value != value:
								setting.update_function(setting.path, setting.name, value)
						except Exception as ex:
							self.error_message = f"Something went wrong: {ex}"

	async def draw_current_page(self, ui, total_available_height):
		if not self.page:
			return
		page = self.pages[self.page]
		# use a single column table with heterogeneous rows later
		if self.error_message:
			ui.strong(self.error_message)
		ui.add_space(10)
		async with egui.ScrollArea.vertical().max_height(total_available_height).show():
			ui.strong(page.title)
			if page.description:
				ui.label(page.description)
			ui.separator()
			for setting in page.settings:
				await self.draw_setting_ui(ui, setting, page)
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