from talon import Module, actions, imgui, app, Context
import os

# we know to stop showing the new user message when the following path is defined
NEW_USER_MESSAGE_DISMISSAL_PATH = os.path.join(os.path.dirname(__file__), "new_user_message_dismissed")

@imgui.open(y=0)
def new_user_gui(gui: imgui.GUI):
	gui.text("Welcome!")
	gui.line()


mod = Module()
mod.tag("new_user_message_showing", desc="The new user message gui is showing")

ctx = Context()

def on_ready():
	if not os.path.exists(NEW_USER_MESSAGE_DISMISSAL_PATH):
		actions.user.new_user_message_show()


app.register("ready", on_ready)

@mod.action_class
class Actions:
	def new_user_message_show():
		"""Shows a useful gui intended for new users"""
		new_user_gui.show()
		ctx.tags = ["user.new_user_message_showing"]

	def new_user_message_hide():
		"""Hides the new user message gui"""
		new_user_gui.hide()
		ctx.tags = []

	def new_user_message_stop_showing_on_startup():
		"""Stops showing the new user message gui on startup"""
		with open(NEW_USER_MESSAGE_DISMISSAL_PATH, "w") as _:
			# this creates an empty file
			pass