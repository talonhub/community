from typing import Optional

from talon import Module, actions, imgui, speech_system

# We keep command_history_size lines of history, but by default display only
# command_history_display of them.
mod = Module()
setting_command_history_size = mod.setting("command_history_size", int, default=50)
setting_command_history_display = mod.setting(
    "command_history_display", int, default=10
)

hist_more = False
history = []


def on_phrase(j):
    global history

    words = j.get("text")

    text = actions.user.history_transform_phrase_text(words)

    if text is not None:
        history.append(text)
        history = history[-setting_command_history_size.get() :]


# todo: dynamic rect?
@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Command History")
    gui.line()
    text = (
        history[:] if hist_more else history[-setting_command_history_display.get() :]
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

        if not actions.speech.enabled():
            return None

        return " ".join(words) if words else None
