from talon import Module, actions, registry

import egui
from ..gui.gui import open_gui

class SpokenForm:
	def __init__(self, text, description, name):
		self.text = text
		self.description = description
		self.name = name

def get_list_description(name):
	return registry.decls.lists[name].desc

def get_capture_description(name):
	try:
		return registry.decls.captures[name].desc
	except KeyError as ex:
		return "Could not find description"

def get_capture_rule(name):
	try:
		capture = registry.captures[name][-1]
		rule = capture.rule
		return rule.rule
	except Exception as ex:
		return "Could not find rule. Something went wrong."

def create_list(name, form_text):
	return SpokenForm(
			form_text,
			get_list_description(name),
			name,
		)

def create_capture(name):
	return SpokenForm(
		get_capture_rule(name),
		get_capture_description(name),
		name,
	)

def compute_spoken_forms(text, exclude_total=True):
	text = text.strip()
	lists = []
	captures = []
	encountered = set()
	start = None
	for i, c in enumerate(text):
		if exclude_total and i == len(text) - 1 and start == 0:
			return []
		if c in ("{", "<"):
			start = i
		elif c == "}":
			form_text = text[start:i+1]
			list_name = form_text[1:-1]
			if form_text not in encountered:
				form = create_list(list_name, form_text)
				lists.append(form)
			encountered.add(form_text)
			start = None
		elif c == ">":
			form_text = text[start:i+1]
			capture_name = form_text[1:-1]
			if form_text not in encountered:
				form = create_capture(capture_name)
				captures.append(form)
			encountered.add(form_text)
			start = None
	return lists, captures



class Expansion:
	def __init__(self):
		self.root = egui.Mutable("")


	async def show_expansion(self, ui, encountered=None, root=None, capture: SpokenForm | None=None):
		if encountered is None:
			encountered = set()
		if root is None:
			root = self.root.get()
			ui.add(egui.TextEdit.singleline(self.root))
		if capture is None:
			title = f"Expansion of {root}"
			show_by_default = True
		else:
			title = f"Capture <{capture.name}>."
			show_by_default = capture.text not in encountered
			encountered.add(capture.text)
		collapsing_header = egui.CollapsingHeader(title).default_open(show_by_default)
		async with ui.group():
			async with ui.scope() as scope, scope.style_mut() as style:
				# make scrollbar always visible when a scroll area is needed
				visuals = style.visuals()
				visuals.indent_has_left_vline = False
				style.set_visuals(visuals)
				async with collapsing_header.show():
					if capture:
						description = capture.description
						if description:
							ui.label(f"Description: {description}")
						async with ui.horizontal_wrapped():
							ui.label(f"Rule: {capture.text}")
							if ui.button("Make root").clicked():
								self.root.set(capture.text)
					lists, captures = compute_spoken_forms(root, exclude_total=False)
					async with ui.horizontal_wrapped():
						if lists:
							ui.label("lists: ")
							for l in lists:
								if ui.button(l.name).clicked():
									pass
					for c in captures:
						await self.show_expansion(ui, encountered, c.text, c)

	async def render(self, ui):
		if self.root.get():
			maximum_height = ui.available_height() - 30
			scroll_area = egui.ScrollArea.vertical().max_height(maximum_height)
			async with scroll_area.show():
				await self.show_expansion(ui) 
		
		if ui.button("hide").clicked():
			actions.user.spoken_form_expansion_hide()

	def show(self, root):
		self.root.set(root)

expansion = None
@open_gui(width=0.5, height=0.5)
async def gui_expansion(ui, ui_wrapper):
	await expansion.render(ui, ui_wrapper)

mod = Module()
@mod.action_class
class Actions:	
	def spoken_form_expansion_show(text: str=""):
		"""Show the spoken form expansion window"""
		actions.user.spoken_form_expansion_hide()
		expansion = Expansion()
		expansion.show(text)
		gui_expansion.show()

	def spoken_form_expansion_hide():
		"""Hide the spoken form expansion window"""
		if gui_expansion.showing():
			gui_expansion.hide()
		if expansion:
			expansion = None