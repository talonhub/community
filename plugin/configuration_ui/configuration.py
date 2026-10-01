#Design:
#	you can use pages showing the settings or do a search
#	1. Setting object including:
#		filepath
#		update method: update the file, handle failure
#		setting/tag name
#		get description from setting and tag name, for default description otherwise get from file
#		get ui vertical size to support heterogeneous rows
#	2. Pages:
#		have a list of setting objects
#		page title, optional description
#		drawn by the overall manager
#	3. Manager:
#		heterogeneous scroll area
#		given an initial width
#		show pages on the left alongside a search feature

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
def compute_commented_tag(line):
	if line.startswith(COMMENTED_TAG_PREFIX):
		return line[len(COMMENTED_TAG_PREFIX):].strip()
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
	value: Any
	description: str
	draw: Callable
	update_function: Callable
	path: Path=SETTINGS_PATH
	compute_vertical_size: Callable=compute_vertical_size_from_number_of_lines_in_description


async def draw_toggle(setting: Setting, ui):
	async with ui.horizontal():
		value = setting.value.get()
		ui.checkbox(setting.value, setting.name)
		ui.label(setting.description)
		new_value = setting.value.get()
		if value != new_value:
			setting.update_function(setting.path, setting.name, new_value)
		
def create_tag_setting(name, description, value):
	return Setting(
		name,
		egui.Mutable(value),
		description,
		draw_toggle,
		update_tag,
	)


@dataclass
class Page:
	title: str
	description: str
	settings: list[Setting]

class Manager:
	def __init__(self):
		pages = [
			Page(
				"Popping",
				"Decide what should happen when you make a popping noise",
				[
					create_tag_setting("user.pop_twice_to_repeat", """# Uncomment below enable pop_twice_to_repeat
# Enabling this tag will repeat the last command when two pops are heard within the allotted time window
# Without this tag noise_trigger_pop is usually associated with pop to click actions
# Enabling this tag disables other pop to click actions in command mode, including pop to click""", False)
				]
			)
		]
		self.pages = {page.title: page for page in pages}
		self.page = ""

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

