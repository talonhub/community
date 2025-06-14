from typing import Optional

from talon import Module, actions, imgui, settings, speech_system

from ..subtitles.on_phrase import skip_phrase

# We keep command_history_size lines of history, but by default display only
# command_history_display of them.
mod = Module()
mod.setting("command_history_size", type=int, default=50)
mod.setting("command_history_display", type=int, default=10)

hist_more: bool = False
history: list[str] = []


def on_phrase(j):
    global history
    if skip_phrase(j):
        return

    words = j.get("phrase")
    text = actions.user.history_transform_phrase_text(words)
    history.append(text)
    history = history[-settings.get("user.command_history_size") :]


# todo: dynamic rect?
@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Command History")
    gui.line()
    text = (
        history[:]
        if hist_more
        else history[-settings.get("user.command_history_display") :]
    )
    for line in text:
        gui.text(line)

    gui.spacer()
    if gui.button("Command history close"):
        actions.user.history_disable()


speech_system.register("phrase", on_phrase)


@mod.action_class
class Actions:
    def history_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def history_enable():
        """Enables the history"""
        gui.show()

    def history_disable():
        """Disables the history"""
        gui.hide()

    def history_clear():
        """Clear the history"""
        global history
        history = []

    def history_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def history_less():
        """Show less history"""
        global hist_more
        hist_more = False

    def history_get(number: int) -> str:
        """returns the history entry at the specified index"""
        num = (0 - number) - 1
        return history[num]

    def history_transform_phrase_text(words: list[str]) -> Optional[str]:
        """Transforms phrase text for presentation in history. Return `None` to omit from history"""
        if words:
            return " ".join(words)
        return None
