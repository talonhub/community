from talon import Module, fs

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

from .gui import open_gui

import egui

@dataclass
class SettingFileSettingInformation:
	value: Any
	description: str

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
	value = line[equals_index+3:]
	name = line[len(prefix):equals_index]
	return name, value

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
				settings[name] = SettingFileSettingInformation(value, "\n".join(description))
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

def update_setting(path, name, value):
	pass

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

@dataclass
class Setting:
	name: str
	draw: Callable
	update_function: Callable
	path: Path=SETTINGS_PATH
	is_tag: bool=False
	value: Any=None
	description: str=""
	compute_vertical_size: Callable=compute_vertical_size_from_number_of_lines_in_description


async def draw_toggle(setting: Setting, ui):
	value = setting.value.get()
	ui.checkbox(setting.value, setting.name)
	ui.label(setting.description)
	new_value = setting.value.get()
	if value != new_value:
		setting.update_function(setting.path, setting.name, new_value)
		
def create_tag_setting(name):
	return Setting(
		name,
		draw_toggle,
		update_tag,
		is_tag=True,
	)


@dataclass
class Page:
	title: str
	description: str
	settings: list[Setting]

def update_setting_information(setting, file_setting_information):
	setting.description = file_setting_information.description
	setting.value = egui.Mutable(file_setting_information.value)

class Manager:
	def __init__(self):
		pages = [
			Page(
				"Popping",
				"Decide what should happen when you make a popping noise",
				[
					create_tag_setting("user.pop_twice_to_repeat"),
					create_tag_setting("user.pop_twice_to_wake")
				]
			)
		]
		self.pages = {page.title: page for page in pages}
		self.page = ""
		self.on_change(SETTINGS_PATH)

	def on_change(self, path):
		tags, settings = parse_settings(path)
		for page in self.pages.values():
			for setting in page.settings:
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
		ui.strong(page.title)
		if page.description:
			ui.label(page.description)
		ui.separator()
		for setting in page.settings:
			await setting.draw(setting, ui)

manager = Manager()

@open_gui(x=0.5, width=0.5, height=0.5, toplevel=False, decorated=True)
async def draw(ui, helpers):
	await manager.draw(ui)

def handle_file_update(path, flags):
	if manager:
		manager.on_change(Path(path))
		draw.refresh()

fs.watch(SETTINGS_PATH, handle_file_update)

mod = Module()
@mod.action_class
class Actions:
	def show_configuration_window():
		"""Show the Community configuration window"""
		draw.show()

	def hide_configuration_window():
		"""Hide the Community configuration window"""
		draw.hide()