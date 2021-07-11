from talon import Module, screen, ui, cron, app, actions, clip
from talon.canvas import Canvas
from typing import Optional
from datetime import datetime
import os

mod = Module()

default_folder = ""
if app.platform == "windows":
    default_folder = os.path.expanduser(os.path.join("~", r"OneDrive\Pictures"))
if not os.path.isdir(default_folder):
    default_folder = os.path.join("~", "Pictures")

screenshot_folder = mod.setting(
    "screenshot_folder",
    type=str,
    default=default_folder,
    desc="Where to save screenshots. Note this folder must exist.",
)


@mod.action_class
class Actions:
    def screenshot(screen_number: Optional[int] = None):
        """Takes a screenshot of the entire screen and saves it to the pictures folder.
        Optional screen number can be given to use screen other than main."""
        screen = get_screen(screen_number)
        screenshot_rect(screen.rect)

    def screenshot_window():
        """Takes a screenshot of the active window and saves it to the pictures folder"""
        win = ui.active_window()
        screenshot_rect(win.rect, win.app.name)

    def screenshot_selection():
        """Triggers an application is capable of taking a screenshot of a portion of the screen"""
        if app.platform == "windows":
            actions.key("super-shift-s")
        elif app.platform == "mac":
            actions.key("ctrl-shift-cmd-4")
        elif app.platform == "linux":
            actions.key("shift-printscr")

    def screenshot_clipboard(screen_number: Optional[int] = None):
        """Takes a screenshot of the entire screen and saves it to the clipboard.
        Optional screen number can be given to use screen other than main."""
        screen = get_screen(screen_number)
        clipboard_rect(screen.rect)

    def screenshot_window_clipboard():
        """Takes a screenshot of the active window and saves it to the clipboard"""
        win = ui.active_window()
        clipboard_rect(win.rect)


def screenshot_rect(rect: ui.Rect, title: str = ""):
    flash_rect(rect)
    img = screen.capture_rect(rect)
    path = get_screenshot_path(title)
    img.write_file(path)


def clipboard_rect(rect: ui.Rect):
    flash_rect(rect)
    img = screen.capture_rect(rect)
    clip.set_image(img)


def get_screenshot_path(title: str = ""):
    if title:
        title = f" - {title.replace('.', '_')}"
    date = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"Screenshot {date}{title}.png"
    folder_path = screenshot_folder.get()
    path = os.path.expanduser(os.path.join(folder_path, filename))
    return os.path.normpath(path)


def flash_rect(rect: ui.Rect):
    def on_draw(c):
        c.paint.style = c.paint.Style.FILL
        c.paint.color = "ffffff"
        c.draw_rect(rect)
        cron.after("150ms", canvas.close)

    canvas = Canvas.from_rect(rect)
    canvas.register("draw", on_draw)
    canvas.freeze()


def get_screen(screen_number: Optional[int] = None) -> ui.Screen:
    if screen_number == None:
        return screen.main_screen()
    return actions.user.screens_get_by_number(screen_number)
