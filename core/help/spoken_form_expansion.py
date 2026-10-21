from talon import Context, Module, actions, registry, cron

import egui
from ..gui.gui import open_gui

from dataclasses import dataclass

@dataclass
class TalonList:
	name: str
	description: str
	number: int

	def __init__(self, name: str, number: int):
		self.name = name
		self.description = get_list_description(name)
		self.number = number

@dataclass
class TalonCapture:
	name: str
	description: str
	number: int
	rule: str
	child_captures: list
	child_lists: list

	def __init__(self, name: str, number: int):
		self.name = name
		self.description = get_capture_description(name)
		self.number = number
		self.rule = get_capture_rule(name)
		self.child_captures = []
		self.child_lists = []
	
	def compute_talon_script_representation(self):
		return f"<{self.name}>"

def get_list_description(name):
	return registry.decls.lists[name].desc

def get_capture_description(name):
	try:
		return registry.decls.captures[name].desc
	except KeyError:
		return "Could not find description"

def get_capture_rule(name):
	try:
		capture = registry.captures[name][-1]
		rule = capture.rule
		return rule.rule
	except Exception:
		return "Could not find rule"

def do_delimiters_conflict(text: str):
	a = text[0]
	b = text[-1]
	return (a == "{") != (b == "}")

def create_spoken_form(text, start, i, create_function, forms, encountered, prior_encountered):
	"""Create the spoken form object at the location. Return the object of a new one is created. Return None if it does not need to be created."""
	form_text = text[start:i+1]
	name = form_text[1:-1]
	if do_delimiters_conflict(form_text):
		raise ValueError(f"Delimiters did not match for {form_text}")
	if form_text in encountered or i - start < 2:
		return None
	if form_text in prior_encountered:
		form = prior_encountered[form_text]
		result = None
	else:
		form = create_function(name, len(prior_encountered) + 1)
		prior_encountered[form_text] = form
		result = form
	forms.append(form)
	encountered.add(form_text)
	return result


def compute_spoken_forms(text, exclude_capture_matching_total=True, prior_encountered_lists=None, prior_encountered_captures=None):
	text = text.strip()
	lists = []
	captures = []
	encountered = set()
	if prior_encountered_lists is None:
		prior_encountered_lists = {}
	if prior_encountered_captures is None:
		prior_encountered_captures = {}

	start = None
	for i, c in enumerate(text):
		if c in ("{", "<"):
			start = i
		elif c == "}":
			create_spoken_form(text, start, i, TalonList, lists, encountered, prior_encountered_lists)
			start = None
		elif c == ">":
			if exclude_capture_matching_total and i == len(text) - 1 and start == 0:
				return [], [], {}, {}
			form = create_spoken_form(text, start, i, TalonCapture, captures, encountered, prior_encountered_captures)
			if form and form.rule:
				form.child_lists, form.child_captures, _, _ = compute_spoken_forms(
					form.rule,
					prior_encountered_lists=prior_encountered_lists,
					prior_encountered_captures=prior_encountered_captures
				)
			start = None
	return lists, captures, prior_encountered_lists, prior_encountered_captures



class Expansion:
	def __init__(self):
		self.root = egui.Mutable("")
		self.new_showing = False
		self.lists = []
		self.captures = []
		self.number_to_list = {}
		self.number_to_capture = {}
		self.history = []

	async def show_expansion(self, ui, encountered=None, root=None, capture: TalonCapture | None=None):
		if encountered is None:
			encountered = set()
		if root is None:
			root = self.root.get()

		async def show_children(lists, captures):
			if capture:
				description = capture.description
				if description:
					ui.label(f"Description: {description}")
				async with ui.horizontal_wrapped():
					ui.label(f"Rule: {capture.rule}")
					if ui.button(f"expansion show {capture.number}").clicked():
						self.set_root_to_child(f"{capture.compute_talon_script_representation()}")
			async with ui.horizontal_wrapped():
				if lists:
					ui.label("lists: ")
					for l in lists:
						if ui.button(f"help list {l.number}: {l.name}").clicked():
							show_list_help(l.name)
			for c in captures:
				await self.show_expansion(ui, encountered, c.rule, c)

		if capture is None:
			if not self.lists and not self.captures:
				return 
			async with ui.group():
				await show_children(self.lists, self.captures)
		else:
			title = f"Capture {capture.compute_talon_script_representation()}."
			show_by_default = capture.name not in encountered
			encountered.add(capture.name)
			collapsing_header = egui.CollapsingHeader(title).default_open(show_by_default)
			async with ui.scope() as scope, scope.style_mut() as style:
				# make scrollbar always visible when a scroll area is needed
				visuals = style.visuals()
				visuals.indent_has_left_vline = False
				style.set_visuals(visuals)
				async with ui.group(), collapsing_header.show():
					await show_children(capture.child_lists, capture.child_captures)


	async def render(self, ui, ui_wrapper):
		async with ui.horizontal_wrapped():
			ui.strong("Spoken form to expand:")
			old_root = self.root.get()
			response = ui.add(egui.TextEdit.singleline(self.root))
			if old_root != self.root.get():
				self.update_expansion()
			if self.new_showing:
				response.request_focus()
				self.new_showing = False
			if self.history and ui_wrapper.button(f"expansion return: {self.history[-1]}"):
				self.set_root_to_parent()
		if self.root.get():
			maximum_height = ui.available_height() - 30
			scroll_area = egui.ScrollArea.vertical().max_height(maximum_height)
			async with scroll_area.show():
				await self.show_expansion(ui) 
		
		if ui.button("expansion close").clicked():
			actions.user.spoken_form_expansion_hide()

	def set_root(self, root):
		self.root.set(root)
		self.update_expansion()

	def set_root_to_child(self, child):
		self.history.append(self.root.get())
		self.set_root(child)

	def set_root_to_parent(self):
		root = self.history.pop()
		self.set_root(root)

	@staticmethod
	def _compute_number_to_spoken_form_dictionary(forms):
		return {f.number: f for f in forms.values()}

	def update_expansion(self):
		self.new_showing = True
		try:
			self.lists, self.captures, all_lists, all_captures = compute_spoken_forms(self.root.get(), exclude_capture_matching_total=False)
		except ValueError:
			self.lists, self.captures, all_lists, all_captures = [], [], {}, {}
		self.number_to_list = self._compute_number_to_spoken_form_dictionary(all_lists)
		self.number_to_capture = self._compute_number_to_spoken_form_dictionary(all_captures)
	

	def get_list(self, number):
		return self.number_to_list.get(number)
			
	def get_capture(self, number):
		return self.number_to_capture.get(number)

def show_list_help(name):
	# doing this in the egui thread freezes Talon
	cron.after("0ms", lambda : actions.user.help_list(name))

expansion = None
@open_gui(width=0.5, height=0.5, always_on_top=False)
async def gui_expansion(ui, ui_wrapper):
	if expansion:
		await expansion.render(ui, ui_wrapper)

mod = Module()
mod.tag("spoken_form_expansion_showing", desc="The spoken form expansion window is showing")
ctx = Context()

@mod.action_class
class Actions:	
	def spoken_form_expansion_show(text: str=""):
		"""Show the spoken form expansion window"""
		global expansion
		actions.user.spoken_form_expansion_hide()
		expansion = Expansion()
		expansion.set_root(text)
		gui_expansion.show()
		ctx.tags = ["user.spoken_form_expansion_showing"]

	def spoken_form_expansion_hide():
		"""Hide the spoken form expansion window"""
		global expansion
		if gui_expansion.showing:
			gui_expansion.hide()
		if expansion:
			expansion = None
		ctx.tags = []

	def spoken_form_expansion_show_help_for_list(number: int):
		"""Show the help for the list with a given number in the spoken form expansion"""
		if target_list := expansion.get_list(number):
			actions.user.help_list(target_list.name)

	def spoken_form_expansion_make_capture_root(number: int):
		"""Show the spoken form expansion for the capture with the given number in the current expansion"""
		if target_list := expansion.get_capture(number):
			expansion.set_root_to_child(target_list.compute_talon_script_representation())

	def spoken_form_expansion_return_to_parent():
		"""Return to showing the spoken form expansion for the parent"""
		expansion.set_root_to_parent()