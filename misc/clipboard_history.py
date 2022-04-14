from typing import Any, List, Optional
from talon import Module, imgui, clip, cron, actions, settings
from talon.skia.image import Image
from dataclasses import dataclass

@dataclass
class ClipItem:
    text: str
    image: Image

mod = Module()
mod.mode("clipboard_history", "Indicates that the clipboard history is visible")

setting_clipboard_history_enabled = mod.setting(
    "clipboard_history_enabled",
    bool,
    default=False,
)
setting_clipboard_history_max_rows = mod.setting(
    "clipboard_history_max_rows",
    type=int,
    default=20,
)
setting_clipboard_history_max_cols = mod.setting(
    "clipboard_manager_max_cols",
    type=int,
    default=50,
)
setting_clipboard_history_polling_intervals = mod.setting(
    "clipboard_history_polling_intervals",
    int,
    default=500,
    desc="Interval in ms between polling clip content",
)

clipboard_history: List[ClipItem] = []

def get_current_clipboard() -> Optional[ClipItem]:
    text = clip.text()

    try:
        image = clip.image()
    except:
        image = None

    if text or image:
        return ClipItem(text, image)
    else:
        return None

def poll_and_update_if_needed():
    last_captured = clipboard_history[0] if len(clipboard_history) > 0 else None
    current_clipboard = get_current_clipboard()
    if last_captured == current_clipboard:
        return
    elif current_clipboard:
        clipboard_history.insert(0, current_clipboard)

    shrink()

if setting_clipboard_history_enabled.get():
    cron.interval(f"{setting_clipboard_history_polling_intervals.get()}ms", poll_and_update_if_needed)

@imgui.open()
def gui(gui: imgui.GUI):
    if not setting_clipboard_history_enabled.get():
        gui.text(f"Clipboard history uses polling")
        gui.text(f"and is disabled by default.")
        gui.text(f"To use globally add the following line to settings.talon:")
        gui.text(f"`user.clipboard_history_enabled = 1`")
        return

    max_rows = setting_clipboard_history_max_rows.get()
    max_cols = setting_clipboard_history_max_cols.get()
    gui.text(f"Clipboard ({len(clipboard_history)} / {max_rows})")
    gui.line()

    for i, item in enumerate(clipboard_history):
        if item.image:
            text = f"Image(width={item.image.width}, height={item.image.height})"
        else:
            text = item.text.replace("\n", "\\n")
            if len(text) > max_cols + 4:
                text = text[:max_cols] + " ..."
        gui.text(f"{i+1}: {text}")

    gui.spacer()
    if gui.button("Clipboard hide"):
        actions.user.clipboard_manager_hide()


@mod.action_class
class Actions:
    def clipboard_history_toggle():
        """Toggle clipboard manager"""
        if gui.showing:
            gui.hide()
        else:
            actions.mode.enable("user.clipboard_history")
            gui.show()

    def clipboard_history_hide():
        """Hide clipboard manager"""
        actions.mode.disable("user.clipboard_history")
        gui.hide()

    def clipboard_history_split(numbers: List[int]):
        """Split clipboard content on new line to add new items to clipboard manager history"""
        for number in numbers:
            validate_number(number)
        new_history = []
        for i, item in enumerate(clipboard_history):
            if i + 1 in numbers and item.text:
                for line in item.text.split("\n"):
                    line = line.strip()
                    if line:
                        new_history.append(ClipItem(line, None))
            else:
                new_history.append(item)
        shrink()

    def clipboard_history_copy(numbers: List[int]):
        """Copy from clipboard history"""
        text, images = get_content(numbers)
        actions.user.clipboard_history_hide()
        if text and images:
            error("Can't copy text and images at once")
        elif len(images) > 1:
            error("Can't copy multiple images at once")
        elif text:
            clip.set_text(text)
        elif images:
            clip.set_image(images[0])

    def clipboard_history_paste(numbers: List[int], match_style: bool = False):
        """Paste from clipboard history"""
        text, images = get_content(numbers)
        actions.user.clipboard_history_hide()
        if text:
            clip.set_text(text)
            if match_style:
                actions.edit.paste_match_style()
            else:
                actions.edit.paste()
        for image in images:
            clip.set_image(image)
            actions.edit.paste()

    def clipboard_history_remove(numbers: List[int] = None):
        """Remove clipboard history"""
        global clipboard_history
        # Remove selected history
        if numbers:
            for number in reversed(sorted(numbers)):
                validate_number(number)
                clipboard_history.pop(number - 1)
        # Remove entire history
        else:
            clipboard_history = []
            actions.user.clipboard_history_hide()

def get_content(numbers: List[int]):
    texts = []
    images = []
    for number in numbers:
        validate_number(number)
        item = clipboard_history[number - 1]
        if item.image:
            images.append(item.image)
        else:
            texts.append(item.text)
    text = "\n".join(texts)
    return text, images


def validate_number(number: range):
    if number < 1 or number > len(clipboard_history):
        error(f"Clipboard manager #{number} is out of range (1-{len(clipboard_history)})")

def shrink():
    global clipboard_history
    max_rows = clip.get()
    if len(clipboard_history) > max_rows:
        clipboard_history = clipboard_history[-max_rows:]


def error(msg: str):
    actions.user.notify(msg)
    raise ValueError(msg)
