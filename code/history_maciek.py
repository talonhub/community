from dearpygui import core, simple
from talon import imgui, Module, speech_system, actions, app

# We keep command_history_size lines of history, but by default display only
# command_history_display of them.
mod = Module()
setting_command_history_size = mod.setting(
    "command_history_size", int, default=50)
setting_command_history_display = mod.setting(
    "command_history_display", int, default=10
)

hist_more = False


def parse_phrase(word_list):
    return " ".join(word.split("\\")[0] for word in word_list)




# todo: dynamic rect?


class HistoryView(object):
    def __init__(self) -> None:
        super().__init__()
        self.history = []
        with simple.window("Example Window"):
            core.add_text("Hello world")
    def on_phrase(self, j):
        print('got', j)

        try:
            val = parse_phrase(getattr(j["parsed"], "_unmapped", j["phrase"]))
        except:
            val = parse_phrase(j["phrase"])

        if val != "":
            self.history.append(val)
            self.history = self.history[-setting_command_history_size.get():]


history_view = HistoryView()
def f():
    core.start_dearpygui()
import threading 
x = threading.Thread(target=f, args=())
x.start()
print(100 * 'done')
speech_system.register("phrase", history_view.on_phrase)
# core.start_dearpy1gui()


@mod.action_class
class Actions:
    def history_maciek_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def history_maciek_enable():
        """Enables the history"""
        gui.show()

    def history_maciek_disable():
        """Disables the history"""
        gui.hide()

    def history_maciek_clear():
        """Clear the history"""
        global history
        history = []

    def history_maciek_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def history_maciek_less():
        """Show less history"""
        global hist_more
        hist_more = False
