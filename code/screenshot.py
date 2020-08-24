from talon import Module, screen, ui, actions, clip, app, settings
from datetime import datetime
import os, subprocess

active_platform = app.platform

mod = Module()
mod.setting(
    "screenshot_folder", type=str, default=None, desc="Where to save screenshots",
)
mod.setting(
    "screenshot_selection_command", type=str, default=None, desc="Custom screenshot command. File path must fit at end",
)

def get_screenshot_path():
    filename = "screenshot-%s.png" % datetime.now().strftime("%Y%m%d%H%M%S")
    folder = settings.get("user.screenshot_folder")
    if folder is None:
        if active_platform == "windows":
            folder = "~" + os.sep + "Desktop"
        elif active_platform == "mac":
            folder = "~"
        elif active_platform == "linux":
            folder = "~"
    to_expand = folder.split(os.sep)
    to_expand.append(filename)
    path = os.path.expanduser(os.path.join(*to_expand))
    return path


@mod.action_class
class Actions:
    def screenshot():
        """takes a screenshot of the entire screen and saves it to the desktop as screenshot.png"""
        img = screen.capture_rect(screen.main_screen().rect)
        path = get_screenshot_path()
        img.write_file(path)
        app.notify(subtitle="Screenshot: %s" % path)

    def screenshot_window():
        """takes a screenshot of the current window and says it to the desktop as screenshot.png"""
        img = screen.capture_rect(ui.active_window().rect)
        path = get_screenshot_path()
        img.write_file(path)
        app.notify(subtitle="Screenshot: %s" % path)

    def screenshot_selection():
        """triggers an application is capable of taking a screenshot of a portion of the screen"""

        if active_platform == "windows":
            actions.key("super-shift-s")
        elif active_platform == "mac":
            actions.key("ctrl-shift-cmd-4")
        elif active_platform == "linux":
            path = get_screenshot_path()
            command = settings.get("user.screenshot_selection_command")
            if command is not None:
                command = command.split(" ")
                command.append(path)
                subprocess.Popen(command)
            else:
                # XXX - make whatever the default is on gnome/kde?
                subprocess.Popen(["scrot", "-s", path])
            app.notify(subtitle="Screenshot: %s" % path)

    def screenshot_clipboard():
        """takes a screenshot of the entire screen and saves it to the clipboard"""
        img = screen.capture_rect(screen.main_screen().rect)
        clip.set_image(img)

    def screenshot_window_clipboard():
        """takes a screenshot of the window and saves it to the clipboard"""
        img = screen.capture_rect(ui.active_window().rect)
        clip.set_image(img)
