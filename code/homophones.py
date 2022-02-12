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


PHONES_FORMATTERS = [
    lambda word: word.capitalize(),
    lambda word: word.upper(),
]


def find_matching_format_function(word_with_formatting, format_functions):
    """ Finds the formatter function from a list of formatter functions which transforms a word into itself.
     Returns an identity function if none exists """
    for formatter in format_functions:
        formatted_word = formatter(word_with_formatting)
        if word_with_formatting == formatted_word:
            return formatter

    return lambda word: word


def raise_homophones(word_to_find_homophones_for, forced=False, selection=False):
    global quick_replace
    global active_word_list
    global show_help
    global force_raise
    global is_selection

    force_raise = forced
    is_selection = selection

    if is_selection:
        word_to_find_homophones_for = word_to_find_homophones_for.strip()

    formatter = find_matching_format_function(word_to_find_homophones_for, PHONES_FORMATTERS)

    word_to_find_homophones_for = word_to_find_homophones_for.lower()

    # We support plurals, but very naively. If we can't find your word but your word ends in an s, presume its plural
    # and attempt to find the singular, then present the presumed plurals back. This could be improved!
    if word_to_find_homophones_for in all_homophones:
        valid_homophones = all_homophones[word_to_find_homophones_for]
    elif word_to_find_homophones_for[-1] == 's' and word_to_find_homophones_for[:-1] in all_homophones:
        valid_homophones = map(lambda w : w + 's', all_homophones[word_to_find_homophones_for[:-1]])
    else:
        app.notify("homophones.py", '"%s" not in homophones list' % word_to_find_homophones_for)
        return

    # Move current word to end of list to reduce searcher's cognitive load
    valid_homophones_reordered = (
        list(
            filter(
                lambda word_from_list: word_from_list.lower() != word_to_find_homophones_for, valid_homophones)
        ) + [word_to_find_homophones_for]
    )
    active_word_list = list(map(formatter, valid_homophones_reordered))

    if (
            is_selection
            and len(active_word_list) == 2
            and quick_replace
            and not force_raise
    ):
        if word_to_find_homophones_for == active_word_list[0].lower():
            new = active_word_list[1]
        else:
            new = active_word_list[0]

        clip.set(new)
        actions.edit.paste()

        return

    actions.mode.enable("user.homophones")
    show_help = False
    gui.show()


@imgui.open(x=main_screen.x + main_screen.width / 2.6, y=main_screen.y)
def gui(gui: imgui.GUI):
    global active_word_list
    if show_help:
        gui.text("Homephone help - todo")
    else:
        gui.text("Select a homophone")
        gui.line()
        index = 1
        for word in active_word_list:
            if gui.button("Choose {}: {}".format(index, word)):
                actions.insert(actions.user.homophones_select(index))
                actions.user.homophones_hide()
            index = index + 1

        if gui.button("Phones hide"):
            actions.user.homophones_hide()


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
        """Show the homophones display"""
        raise_homophones(m, False, False)

    def homophones_show_selection():
        """Show the homophones display for the selected text"""
        raise_homophones(actions.edit.selected_text(), False, True)

    def homophones_force_show(m: str):
        """Show the homophones display forcibly"""
        raise_homophones(m, True, False)

    def homophones_force_show_selection():
        """Show the homophones display for the selected text forcibly"""
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

    def homophones_get(word: str) -> [str] or None:
        """Get homophones for the given word"""
        word = word.lower()
        if word in all_homophones:
            return all_homophones[word]
        return None
