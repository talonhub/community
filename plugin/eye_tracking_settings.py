from talon import app, ui, screen
from talon.track.geom import Point2d
from talon_plugins import eye_zoom_mouse


eye_zoom_mouse.config.center_zoom = True
eye_zoom_mouse.config.toggle_speech_when_zoomed = True
eye_zoom_mouse.config.enable_hiss_for_right_click = True
eye_zoom_mouse.config.hide_cursor_for_control_mouse = False


def on_ready():
    on_screen_change(None)


def on_screen_change(screens: list[screen.Screen]) -> None:
    if app.platform == "mac":
        width = (int)(ui.main_screen().width * 0.10)
        height = (int)(ui.main_screen().height * 0.15)
        eye_zoom_mouse.config.screen_area = Point2d(width, height)
        eye_zoom_mouse.config.img_scale = 6
    elif app.platform == "windows":
        width = (int)(ui.main_screen().width * 0.10)
        height = (int)(ui.main_screen().height * 0.125)
        eye_zoom_mouse.config.screen_area = Point2d(width, height)
        eye_zoom_mouse.config.img_scale = 6


ui.register("screen_change", on_screen_change)
app.register("ready", on_ready)
