from typing import Any, List
from talon import Module, imgui, clip, cron, actions, settings

mod = Module()

clip_history_max_symbols_per_line = mod.setting("clip_history_max_symbols_per_line", int, default=30)
clip_history_max_lines = mod.setting("clip_history_max_lines", int, default=10)
clip_history_polling_intervals = mod.setting("clip_history_polling_intervals", int, default=100, desc="Interval in ms between polling clip content")

last_serial: int = 0
clip_history: List[Any] = []

def clip_history_update_if_needed():
    global last_serial
    if clip.serial() != last_serial:
        last_serial = clip.serial()
        if clip.text():
            clip_history.insert(0, clip.text())
        else:
            try:
                image = clip.image()
                clip_history.insert(0, image)
            except:
                None

        if len(clip_history) > clip_history_max_lines.get():
            clip_history.pop()

cron.interval(f"{clip_history_polling_intervals.get()}ms", clip_history_update_if_needed)   

@imgui.open(y=0)
def gui_clip_history(gui: imgui.GUI):
    gui.text("Clip history. `Paste at <index>`")
    gui.line()
    for idx, history_entry in enumerate(clip_history):
        if isinstance(history_entry, str):
            max_characters_per_line = clip_history_max_symbols_per_line.get()
            if len(history_entry) > max_characters_per_line:
                truncated_history_entry = history_entry[:max_characters_per_line] + "..."
            else:
                truncated_history_entry = history_entry
            gui.text(f"{idx}. {truncated_history_entry}")
        else:
            # imgui.GUI does not seem to support drawing an image
            gui.text(f"{idx}. <image you copied>")

@mod.action_class
class ClipActions:
    def clip_history():
        """Show clip history"""
        if gui_clip_history.showing:
            gui_clip_history.hide()
        else:
            gui_clip_history.show()

    def paste_from_history(index: int):
        """Paste from history at index"""
        global last_serial

        if len(clip_history) <= index:
            return 

        to_paste = clip_history.pop(index)
        if isinstance(to_paste, str):
            clip.set_text(to_paste)
        else:
            clip.set_image(to_paste)
        last_serial = clip.serial()
        actions.edit.paste()
        clip_history.insert(0, to_paste)