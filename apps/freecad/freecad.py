from talon import Context, Module, actions, app

ctx = Context()
mod = Module()
apps = mod.apps
apps.freecad = "app.name: FreeCAD"
apps.firefox = """
os: mac
and app.bundle: org.freecad.fcst
"""

mod.list("freecad_view", desc="List of FreeCAD views")
mod.list("freecad_geometry", desc="List of FreeCAD geometry")
mod.list("freecad_constraints", desc="List of FreeCAD constraints")

# @mod.action_class
# class Actions:
#     def firefox_bookmarks_sidebar():
#         """Toggles the Firefox bookmark sidebar"""

#     def firefox_history_sidebar():
#         """Toggles the Firefox history sidebar"""


# @ctx.action_class("user")
# class UserActions:
#     def tab_close_wrapper():
#         actions.sleep("180ms")
#         actions.app.tab_close()


# @ctx.action_class("browser")
# class BrowserActions:
#     def focus_page():
#         actions.browser.focus_address()
#         actions.edit.find()
#         actions.sleep("180ms")
#         actions.key("escape")

#     def go_home():
#         actions.key("alt-home")
