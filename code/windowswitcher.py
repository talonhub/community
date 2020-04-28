from talon import Context, Module, app, clip, cron, imgui, actions, ui
from .keys import default_alphabet, letters_string

from math import log, ceil

ctx = Context()

mod = Module()
mod.list('window_selection_words', desc='list of words ')
mod.list('homophones_selections', desc='list of valid selection indexes')

@mod.capture
def window_selection_words(m) -> int:
    "Returns the index of the aplication selected via letter words"

shown_windows = []
window_codes = []
window_spelling = []

@imgui.open(y=0,software=True)
def gui(gui: imgui.GUI):
    global shown_windows
    gui.text("Select a window")
    gui.line()
    index = 0
    for win in shown_windows:
        gui.text("switch {}: {} ({})".format(window_spelling[index],win.title, win.app.name))
        index = index + 1
    
    if gui.button("close"):
        gui.hide()

def make_combinations(amount):
    base_pieces = len(default_alphabet)
    base_num = ceil(log(amount, base_pieces))

    pieces = [0] * base_num
    results = []
    results.append(list(pieces))
    for entry in range(0, amount):
        for pos in range(base_num - 1, -1, -1):
            pieces[pos] += 1
            if pieces[pos] == base_pieces:
                pieces[pos] = 0
            else:
                break
        results.append(list(pieces))

    return results

@mod.action_class
class Actions:
    def show_window_switcher():
        """Display a window switcher"""
        global shown_windows
        global window_codes
        global window_spelling

        shown_windows = ui.windows()

        combs = make_combinations(len(shown_windows))

        window_spelling = list(map(lambda entry: " ".join(map(lambda digit: default_alphabet[digit], entry)), combs))
        ctx.lists['self.window_selection_words'] = window_spelling

        window_codes = list(map(lambda entry: map(lambda digit: letters_string[digit], entry), combs))

        gui.show()

    def switch_to_window(window: ui.Window):
        """Switch to the window at the given index"""
        global shown_windows
        global window_codes
        global window_spelling
        window.focus()
        gui.hide()
        shown_windows = []
        window_codes = []
        window_spelling = []

@ctx.capture(rule='{self.window_selection_words}')
def window_selection_words(m):
    taken = window_spelling.index(m.window_selection_words)
    return shown_windows[taken]

ctx.lists['self.window_selection_words'] = []
