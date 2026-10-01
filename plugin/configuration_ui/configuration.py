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
from typing import Callable

import egui

def update_setting(path, name, value):
	pass

def update_tag(path, name, should_be_active):
	pass

@dataclass
class Setting:
	path: Path
	name: str
	description: str
	compute_vertical_size: Callable
	draw: Callable
	update_function: Callable=update_setting

@dataclass
class Page:
	title: str
	settings: list[Setting]
	description: str=""

class Manager:
	def __init__(self):
		pages = []
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

