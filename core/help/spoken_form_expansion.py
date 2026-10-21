from talon import Context, Module, actions, registry, cron

import egui
from ..gui.gui import open_gui, let_user_use_page_keys_to_scroll_scroll_area

from dataclasses import dataclass, field

@dataclass
class TalonList:
	"""Information on a Talon list used to represent it graphically in the expansion"""
	name: str
	id_number: int

	def __init__(self, name: str, number: int):
		self.name = name
		self.id_number = number

	def create_children(self, callback):
		# lists have no children
		pass

@dataclass
class SpokenFormChildren:
	"""The children of a parent spoken form"""
	lists: list = field(default_factory=list)
	captures: list = field(default_factory=list)

	def is_empty(self):
		return not self.lists or not self.captures

@dataclass
class TalonCapture:
	"""Information on a Talon capture used to represent it graphically in the expansion"""
	name: str
	description: str | None
	id_number: int
	rule: str
	children: SpokenFormChildren

	def __init__(self, name: str, number: int):
		self.name = name
		self.description = get_capture_description(name)
		self.id_number = number
		self.rule = get_capture_rule(name)
		self.children = SpokenFormChildren()

	def create_children(self, callback):
		if self.rule:
			self.children = callback(self.rule)
	
	def compute_talon_script_representation(self):
		return f"<{self.name}>"

def get_capture_description(name):
	try:
		return registry.decls.captures[name].desc
	except KeyError:
		return None

def get_capture_rule(name):
	try:
		capture = registry.captures[name][-1]
		rule = capture.rule
		return rule.rule
	except Exception:
		return None

def do_delimiters_conflict(text: str):
	# the only relevant delimiters are angle brackets and curly braces
	# this checks if the delimiters at the start and end match using that assumption
	a = text[0]
	b = text[-1]
	return (a == "{") != (b == "}")

def compute_number_to_spoken_form_dictionary(forms):
	return {f.number: f for f in forms.values()}

def get_description_or_default(description):
	if not description:
		return "Could not find description"
	return description

def get_rule_or_default(rule):
	if not rule:
		return "Could not find rule"
	return rule

class SpokenFormTree:
	"""Represents the spoken form tree starting with the child spoken forms in the given text"""
	def __init__(self, text):
		self._all_lists = {}
		self._all_captures = {}
		self.children = self._compute_spoken_forms(text)
		self.number_to_list = compute_number_to_spoken_form_dictionary(self._all_lists)
		self.number_to_capture = compute_number_to_spoken_form_dictionary(self._all_captures)
		# these were used for the calculations but are not needed after construction
		del self._all_lists
		del self._all_captures
	
	def _create_spoken_form(self, text, start, i, create_function, forms, encountered_at_this_level, prior_encountered):
		"""Create the spoken form object at the location. Raises ValueError with invalid delimiters."""
		if start is None:
			raise ValueError(f"Encountered closing delimiter {start[i]} with no opening delimiter in {text}!")
		form_text = text[start:i+1]
		name = form_text[1:-1]
		if do_delimiters_conflict(form_text):
			raise ValueError(f"Delimiters did not match for {form_text}")
		# avoid redundancy at the current level. There is no point in listing a list or capture as the child of a spoken form multiple times just because it uses them multiple times. 
		if form_text in encountered_at_this_level or i - start < 2:
			return
		# reuse values when possible to improve time and memory efficiency
		# this avoids having to recompute the children of a capture every time it is encountered
		# nonetheless, if something encountered before is a child of a spoken form, it needs to be shown as one of its children, so still add it to the list of forms encountered at this level
		form = prior_encountered.get(form_text)
		if form is None:
			form = create_function(name, len(prior_encountered) + 1)
			form.create_children(self._compute_spoken_forms)
			prior_encountered[form_text] = form
		forms.append(form)
		encountered_at_this_level.add(form_text)


	def _compute_spoken_forms(self, text):
		"""Identify the lists and captures that are children of the given text."""
		children = SpokenFormChildren()
		encountered_at_this_level = set()

		start = None
		for i, c in enumerate(text):
			if c in ("{", "<"):
				start = i
			elif c == "}":
				self._create_spoken_form(text, start, i, TalonList, children.lists, encountered_at_this_level, self._all_lists)
				start = None
			elif c == ">":
				self._create_spoken_form(text, start, i, TalonCapture, children.captures, encountered_at_this_level, self._all_captures)
				start = None
		return children

	def is_empty(self):
		return not self.children.is_empty()

class TreeRenderer:
	def __init__(self, set_root_to_child_callback, update_tree_callback, set_root_to_parent_callback):
		"""Used to let the user input a spoken form and render its tree"""
		self._encountered_this_render = set()
		self._set_root_to_child_callback = set_root_to_child_callback
		self._update_tree_callback = update_tree_callback
		self._set_root_to_parent_callback = set_root_to_parent_callback
		self._ui = None
		self._ui_wrapper = None

	async def render_capture_ui(self, capture):
		"""Renders information about the capture"""
		if capture.description is None and capture.rule is None and capture.children.is_empty():
			self._ui.label("Could not find information on this capture.")
			return 
		description = capture.description
		if description is not None:
			description = get_description_or_default(description)
			self._ui.label(f"Description: {description}")
		async with self._ui.horizontal_wrapped():
			rule = get_rule_or_default(capture.rule)
			self._ui.label(f"Rule: {rule}")
			if self._ui_wrapper.button(f"expansion show {capture.number}"):
				self._set_root_to_child_callback(f"{capture.compute_talon_script_representation()}")
		await self.render_children(capture.children)

	async def render_capture_card(self, capture):
		"""Renders the card around the capture ui"""
		title = f"Capture {capture.compute_talon_script_representation()}."
		expand_by_default = capture.name not in self._encountered_this_render
		self._encountered_this_render.add(capture.name)
		collapsing_header = egui.CollapsingHeader(title).default_open(expand_by_default)
		async with self._ui.scope() as scope, scope.style_mut() as style:
			# do not render vertical line for the collapsing header
			visuals = style.visuals()
			visuals.indent_has_left_vline = False
			style.set_visuals(visuals)
			async with self._ui.group(), collapsing_header.show():
				await self.render_capture_ui(capture)

	async def render_lists(self, lists):
		"""Render a list of Talon lists"""
		if lists:
			async with self._ui.horizontal_wrapped():
				self._ui.label("lists: ")
				for l in lists:
					if self._ui_wrapper.button(f"help list {l.number}: {l.name}"):
						open_list_help(l.name)

	async def render_children(self, children):
		"""Render the children of a current spoken"""
		await self.render_lists(children.lists)
		for c in children.captures:
			await self.render_capture_card(c)

	async def render_expansion_tree(self, tree):
		"""Render a spoken form expansion tree"""
		if not tree or tree.is_empty():
			return 
		async with self._ui.group():
			await self.render_children(tree.children)
		self._encountered_this_render.clear()

	async def renderer_header(self, root, history, is_rendering_new_tree):
		async with self._ui.horizontal_wrapped():
			self._ui.strong("Spoken form to expand:")
			old_root = root.get()
			response = self._ui.add(egui.TextEdit.singleline(root))
			if old_root != root.get():
				self._update_tree_callback()
			if is_rendering_new_tree:
				response.request_focus()
			if history and self._ui_wrapper.button(f"expansion return: {history[-1]}"):
				self._set_root_to_parent_callback()

	async def render_bottom_buttons(self):
		async with self._ui.with_layout(egui.Layout.bottom_up(egui.Align.Center)):
			async with self._ui.horizontal_wrapped():
				if self._ui.button("expansion close").clicked():
					actions.user.spoken_form_expansion_hide()
				if self._ui_wrapper.button("page down"):
					actions.key("pagedown")
				if self._ui_wrapper.button("page up"):
					actions.key("pageup")
			self._ui.separator()

	async def render(self, ui, ui_wrapper, root: egui.Mutable[str], tree, history: list[str], is_rendering_new_tree: bool):
		"""Render the ui for and putting a spoken form and seeing the resulting expansion tree"""
		self._ui = ui
		self._ui_wrapper = ui_wrapper
		await self.renderer_header(root, history, is_rendering_new_tree)
		if root.get() and tree:
			maximum_height = ui.available_height() - 30
			scroll_area = egui.ScrollArea.vertical().max_height(maximum_height)
			async with scroll_area.show() as scroll_ui:
				await let_user_use_page_keys_to_scroll_scroll_area(scroll_ui)
				await self.render_expansion_tree(tree)
		await self.render_bottom_buttons()
		self._ui = None
		self._ui_wrapper = None

class TreeManager:
	def __init__(self, refresh_callback):
		self._root = egui.Mutable("")
		self._is_rendering_new_tree = True
		self._tree = None
		self._history = []
		self._tree_renderer = TreeRenderer(self.set_root_to_child, self.update_tree, self.set_root_to_parent)
		self._refresh_callback = refresh_callback

	async def render(self, ui, ui_wrapper):
		await self._tree_renderer.render(ui, ui_wrapper, self._root, self._tree, self._history, self._is_rendering_new_tree)
		self._is_rendering_new_tree = False

	def set_root(self, root):
		self._root.set(root)
		self.update_tree()

	def set_root_to_child(self, child):
		self._history.append(self._root.get())
		self.set_root(child)

	def set_root_to_parent(self):
		root = self._history.pop()
		self.set_root(root)

	def update_tree(self):
		self._is_rendering_new_tree = True
		try:
			self._tree = SpokenFormTree(self._root.get())
		except ValueError:
			self._tree = None
		self._refresh_callback()

	def get_list(self, number):
		if not self._tree:
			return None
		return self._tree.number_to_list.get(number)
			
	def get_capture(self, number):
		if not self._tree:
			return None
		return self._tree.number_to_capture.get(number)

def open_list_help(name):
	# doing this in the egui thread freezes Talon
	cron.after("0ms", lambda : actions.user.help_list(name))

expansion = None
@open_gui(width=0.75, height=0.75, always_on_top=False)
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
		expansion = TreeManager(gui_expansion.refresh)
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