from typing import Optional
from datetime import datetime
from talon import Module, actions, imgui, settings, speech_system, clip

# We keep rejection_history_size lines of history, but by default display only
# rejection_history_display of them.
mod = Module()
mod.setting("rejection_history_size", type=int, default=50)
mod.setting("rejection_history_display", type=int, default=10)

hist_more = False
history = []
history_no_timestamp = []

def on_phrase(j):
    global history, history_no_timestamp
    meta = j['_metadata']
    if meta['reject']:
        print(f"Rejected: {meta['emit']} {datetime.now()}")
        hypothesis = f"{meta['emit']}"

        history.append(f"{hypothesis} {datetime.now()}" if len (hypothesis) > 0 else f"Noise rejected {datetime.now()}")
        history_no_timestamp.append(f"{hypothesis}")
        history_no_timestamp = history_no_timestamp[-settings.get("user.rejection_history_size") :]
        history = history[-settings.get("user.rejection_history_size") :]


# todo: dynamic rect?
@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Rejection History")
    gui.line()
    text = (
        history[:]
        if hist_more
        else history[-settings.get("user.rejection_history_display") :]
    )
    for line in text:
        gui.text(line)

    gui.spacer()
    if gui.button("Rejection history close"):
        actions.user.rejection_history_disable()


speech_system.register("phrase", on_phrase)


@mod.action_class
class Actions:
    def rejection_history_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def rejection_history_enable():
        """Enables the history"""
        gui.show()

    def rejection_history_disable():
        """Disables the history"""
        gui.hide()

    def rejection_history_clear():
        """Clear the history"""
        global history
        history = []

    def rejection_history_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def rejection_history_less():
        """Show less history"""
        global hist_more
        hist_more = False

    def rejection_history_get(number: int) -> str:
        """returns the history entry at the specified index"""
        num = (0 - number) - 1
        return history[num]

    def rejection_history_transform_phrase_text(words: list[str]) -> Optional[str]:
        """Transforms phrase text for presentation in history. Return `None` to omit from history"""

        if not actions.speech.enabled():
            return None

        return " ".join(words) if words else None
    
    def rejection_copy_last():
        """placeholder"""
        clip.set_text(history_no_timestamp[-1])
        
