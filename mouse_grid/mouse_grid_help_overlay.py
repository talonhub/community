from talon import Module, Context, imgui, screen, settings, storage

mod = Module()

@imgui.open()
def help_overlay(gui: imgui.GUI):
    gui.text("Mouse Grid Usage")
    gui.line()

    gui.text("Say any of the nine numbers to narrow down")
    gui.text("where you want the mouse to go")
    gui.text("")

    gui.text(" - grid off (hides grid)")
    gui.text(" - grid reset (go back to the start)")
    gui.text(" - grid back (go back one step)")

    gui.text("")

    gui.text(" - touch (left click)")
    gui.text(" - righty (right click)")
    gui.text(" - mid click (middle click)")

    gui.text("")

    gui.text("combiners like shift, control, etc can")
    gui.text("go in front of the click commands")

    gui.text("")

    gui.text(" - dub click / duke (double click)")
    gui.text(" - trip click (triple click)")
    gui.text(" - drag (to start/stop dragging left mouse button)")

    gui.text("")

    gui.text(" - mouse grid help hide (close this help text)")
    gui.text(" - mouse grid help disable (not see this help text again)")
    gui.text(" - mouse grid help enable (to turn this back on)")
    gui.text(" - mouse grid help (bring this help text back)")

    gui.text("")

    if gui.button("close"):
        help_overlay.hide()

    if gui.button("disable"):
        help_overlay.hide()
        storage.set("mouse_grid_help_overlay_activated", False)

try:
    storage.get("mouse_grid_help_overlay_activated")
except KeyError:
    storage.set("mouse_grid_help_overlay_activated", True)

@mod.action_class
class MouseGridHelpOverlay:
    def mouse_grid_help_overlay_force_show():
        """Bring up the mouse grid help overlay (wether or not it's enabled)"""
        help_overlay.show()
    def mouse_grid_help_overlay_show():
        """Bring up the mouse grid help overlay (if it is enabled)"""
        if storage.get("mouse_grid_help_overlay_activated"):
            help_overlay.show()

    def mouse_grid_help_overlay_close():
        """Hides the mouse grid help overlay"""
        help_overlay.hide()

    def mouse_grid_help_overlay_disable():
        """Disables the mouse grid help overlay"""
        storage.set("mouse_grid_help_overlay_activated", False)

    def mouse_grid_help_overlay_enable():
        """Enables the mouse grid help overlay"""
        storage.set("mouse_grid_help_overlay_activated", True)

