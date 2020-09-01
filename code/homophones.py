from talon import Context, Module, app, clip, cron, imgui, actions, ui, fs
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
mod = Module()
mod.mode("homophones")
mod.list("homophones_canonicals", desc="list of words ")


main_screen = ui.main_screen()


def update_homophones(name, flags):
    global phones, canonical_list, all_homophones
    phones = {}
    canonical_list = []
    if name is None or name == homophones_file:
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
    # print(str(canonical_list))
    ctx.lists["self.homophones_canonicals"] = canonical_list


update_homophones(None, None)
fs.watch(cwd, update_homophones)
active_word_list = None
is_selection = False


def close_homophones():
    gui.hide()
    actions.mode.disable("user.homophones")


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

    actions.mode.enable("user.homophones")
    show_help = False
    gui.freeze()


@imgui.open(y=0, x=main_screen.width / 2.6, software=False)
def gui(gui: imgui.GUI):
    global active_word_list
    if show_help:
        gui.text("Homephone help - todo")
    else:
        gui.text("Select a homophone")
        gui.line()
        index = 1
        for word in active_word_list:
            gui.text("Pick {}: {} ".format(index, word))
            index = index + 1


def show_help_gui():
    global show_help
    show_help = True
    gui.freeze()


@mod.capture
def homophones_canonical(m) -> str:
    "Returns a single string"


@mod.action_class
class Actions:
    def homophones_hide():
        """Hides the homophones display"""
        close_homophones()

    def homophones_show(m: str):
        """Sentence formatter"""
        raise_homophones(m, False, False)

    def homophones_show_selection():
        """Sentence formatter"""
        raise_homophones(actions.edit.selected_text(), False, True)

    def homophones_force_show(m: str):
        """Sentence formatter"""
        raise_homophones(m, True, False)

    def homophones_force_show_selection():
        """Sentence formatter"""
        raise_homophones(actions.edit.selected_text(), True, True)

    def homophones_select(number: int) -> str:
        """selects the homophone by number"""
        if number <= len(active_word_list) and number > 0:
            return active_word_list[number - 1]

        error = "homophones.py index {} is out of range (1-{})".format(
            number, len(active_word_list)
        )
        app.notify(error)
        raise error


@ctx.capture(rule="{self.homophones_canonicals}")
def homophones_canonical(m):
    return m.homophones_canonicals
