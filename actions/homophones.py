from talon import Context, Module, app, clip, cron, imgui, actions
from talon.voice import Capture
from ..utils import parse_word
import os

########################################################################
# global settings
########################################################################

# a list of homophones where each line is a comma separated list
# e.g. where,wear,ware
# a suitable one can be found here:
# https://github.com/pimentel/homophones
cwd = os.path.dirname(os.path.realpath(__file__))
homophones_file = os.path.join(cwd, "homophones.csv")
# if quick_replace, then when a word is selected and only one homophone exists,
# replace it without bringing up the options
quick_replace = True
show_help = False
########################################################################

ctx = Context()

phones = {}
canonical_list = []
with open(homophones_file, "r") as f:
    for h in f:
        h = h.rstrip()
        h = h.split(",")
        canonical_list.append(max(h, key=len))
        for w in h:
            w = w.lower()
            others = phones.get(w, None)
            if others is None:
                phones[w] = sorted(h)
            else:
                # if there are multiple hits, collapse them into one list
                others += h
                others = set(others)
                others = sorted(others)
                phones[w] = others

all_homophones = phones

active_word_list = None
is_selection = False

def close_homophones():
    ctx.lists['self.selections'] = []
    gui.hide()

def make_selection(index: int):
    global active_word_list
    cron.after("0s", close_homophones)
    if is_selection:
        clip.set(active_word_list[index - 1])

    actions.insert(active_word_list[index - 1])
    

def raise_homophones(word, forced=False, selection=False):
    global quick_replace
    global active_word_list
    global show_help
    global force_raise
    global is_selection 

    force_raise = forced
    is_selection = selection
    
    if is_selection:
        word = word.strip()

    is_capitalized = word == word.capitalize()
    is_upper = word.isupper()

    word = word.lower()

    if word not in all_homophones:
        app.notify("homophones.py", '"%s" not in homophones list' % word)
        return

    active_word_list = all_homophones[word]
    if (
        is_selection
        and len(active_word_list) == 2
        and quick_replace
        and not force_raise
    ):
        if word == active_word_list[0].lower():
            new = active_word_list[1]
        else:
            new = active_word_list[0]

        if is_capitalized:
            new = new.capitalize()
        elif is_upper:
            new = new.upper()

        clip.set(new)
        actions.edit.paste()

        return

    index = 1
    selections = []
    for word in active_word_list:
        selections.append(str(index))
        index = index + 1 
    ctx.lists['self.selections'] = selections

    show_help = False
    gui.show()

@imgui.open(rect=imgui.Rect(1400, 750, 250, 500))
def gui(gui: imgui.GUI):
    global active_word_list
    if show_help:
        gui.text("Homephone help - todo")
    else:
        gui.text("Select a homophone")
        gui.line()
        index = 1
        for word in active_word_list:
            gui.text("Pick {}: {} ".format(index,word))
            index = index + 1

def show_help_gui():
    global show_help
    show_help = True
    gui.show()

mod = Module()
mod.list('canonicals', desc='list of words ')
mod.list('selections', desc='list of valid selection indexes')

@mod.capture
def canonical(m) -> str:
    "Returns a single string"

@mod.capture 
def selection(m) -> int:
    "Returns a single integer (1-based)"

@mod.action_class
class Actions:
    def show_homophones_help():
        """Shows help"""
        show_help_gui()

    def hide_homophones():
        """Hides the homophones display"""
        close_homophones()

    def show_homophones(m: str):
        """Sentence formatter"""
        raise_homophones(m, False, False)

    def show_homophones_selection():
        """Sentence formatter"""
        actions.edit.copy()
        raise_homophones(clip.get(), False, True)

    def force_show_homophones(m: str):
        """Sentence formatter"""
        raise_homophones(m, True, False)

    def force_show_homophones_selection():
        """Sentence formatter"""
        actions.edit.copy()
        raise_homophones(clip.get(), True, True)

    def format_selection(word: str, fmtrs: list):
        """Formats the selection using Formatters"""
        user.actions.formatters.formatters.format_words([word], fmtrs)

        
@ctx.capture(rule='{self.canonicals}')
def canonical(m):
    print(str(m.canonicals))
    return m.canonicals[-1]

@ctx.capture(rule='{self.selections}')
def selection(m):
    global active_word_list
    return active_word_list[int(m.selections[-1]) - 1]

ctx.lists['self.canonicals'] = canonical_list
ctx.lists['self.selections'] = []
