# from nriley/knausj_talon

from talon import actions, app, Module, ui

mod = Module()

@mod.action_class
class Actions:
	def launch_bundle(bundle: str):
		"""Launch an application by bundle ID."""
		ui.launch(bundle=bundle)

	def focus_bundle(bundle: str):
		"""Focus and return an application by bundle ID, or None if unable to do so."""
		active_app = ui.active_app()
		if active_app.bundle == bundle:
			return active_app
		try:
			ui.apps(bundle=bundle)[0].focus()
		except IndexError:
			return None
		for attempt in range(10):
			active_app = ui.active_app()
			if active_app.bundle == bundle:
				return active_app
			actions.sleep("50ms")
		app.notify(title='Failed to focus application',
				   body=f'Bundle ID: {bundle}')
		return None

	def launch_or_focus_bundle(bundle: str):
		"""Launch or focus and return an application by bundle ID, or None if unable to do so."""
		app = actions.user.focus_bundle(bundle)
		if app is not None:
			return app
		actions.user.launch_bundle(bundle)
		for attempt in range(100):
			active_app = ui.active_app()
			if active_app.bundle == bundle:
				return active_app
			actions.sleep("50ms")
		return actions.user.focus_bundle(bundle)