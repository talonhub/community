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
    if name != homophones_file:
        return

    phones = {}
    canonical_list = []
    with open(homophones_file, "r") as f:
        for line in f:
            words = line.rstrip().split(",")
            canonical_list.append(words[0])
            for word in words:
                word = word.lower()
                old_words = phones.get(word, [])
                phones[word] = sorted(set(old_words + words))

    global all_homophones
    all_homophones = phones
    ctx.lists["self.homophones_canonicals"] = canonical_list


update_homophones(homophones_file, None)
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
    gui.show()


@imgui.open(y=0, x=main_screen.width / 2.6)
def gui(gui: imgui.GUI):
    global active_word_list
    if show_help:
        gui.text("Homephone help - todo")
    else:
        gui.text("Select a homophone")
        gui.line()
        index = 1
        for word in active_word_list:
            gui.text("Choose {}: {} ".format(index, word))
            index = index + 1


def show_help_gui():
    global show_help
    show_help = True
    gui.show()


@mod.capture(rule="{self.homophones_canonicals}")
def homophones_canonical(m) -> str:
    "Returns a single string"
    return m.homophones_canonicals


@mod.action_class
class Actions:
    def homophones_hide():
        """Hides the homophones display"""
        close_homophones()

    def homophones_show(m: str):
        """Sentence formatter"""
        print(m)
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

