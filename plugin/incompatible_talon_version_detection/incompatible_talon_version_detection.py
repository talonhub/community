from talon import app, imgui, actions

def compute_version_number() -> float:
	version = app.version
	decimal_points = 0
	i = 0
	while i < len(version) and (version[i] == "." or version[i].isdigit()):
		if version[i] == ".":
			decimal_points += 1
			if decimal_points > 1:
				break
		i += 1
	if i == 0:
		raise ValueError(f"Could not parse Talon version {version}")
	return float(version[:i])

def on_ready():
	if compute_version_number() < 1:
		@imgui.open()
		def gui(gui: imgui.GUI):
			gui.text("You are using a version of the Community maintained voice command set")
			gui.text("intended for Talon 1.0 on an older version of Talon.")
			gui.text("The following button takes you to a page where you can download a")
			gui.text("version compatible with Talon 0.4")
			if gui.button("open zero point four download link"):
				actions.user.open_url("https://github.com/talonhub/community/releases/tag/v0.4")
				hide_ui()
			if gui.button("dismiss version message"):
				hide_ui()
		def hide_ui():
			gui.hide()
		gui.show()


app.register("ready", on_ready)