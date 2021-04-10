import logging
import os
import shutil
import warnings
from pathlib import Path

from talon import Context, Module, actions, app, clip, cron, imgui, resource, ui

from .user_settings import DATA_DIR, SETTINGS_DIR

########################################################################
# global settings
########################################################################
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


def get_homophones_from_csv(filename: str):
    """Retrieves homophones from CSV"""
    # todo this code could be consolidated, save for parsing, with user_settings.
    path = SETTINGS_DIR / filename
    template_name = filename + ".template"
    template_path = DATA_DIR / template_name
    cwd = os.path.dirname(os.path.realpath(__file__))
    legacy_path = Path(os.path.join(cwd, "homophones.csv"))
    # print(str(legacy_path))
    assert filename.endswith(".csv")
    if not path.is_file():
        if legacy_path and legacy_path.is_file():
            shutil.move(legacy_path, path)
            warnings.warn(
                "Support for the legacy CSVs location (i.e. outside /Settings) will be removed in the Talon v0.2.0 timeframe. Moving file from {} to {}".format(
                    legacy_path, path
                ),
                DeprecationWarning,
            )
        else:
            assert template_path.is_file()
            shutil.copyfile(template_path, path)

    phones = {}
    canonical_list = []
    with resource.open(path, "r") as f:
        for line in f:
            words = line.rstrip().split(",")
            canonical_list.append(words[0])
            for word in words:
                word = word.lower()
                old_words = phones.get(word, [])
                phones[word] = sorted(set(old_words + words))

    global all_homophones
    all_homophones = phones
    return canonical_list


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


def on_ready():
    ctx.lists["self.homophones_canonicals"] = get_homophones_from_csv("homophones.csv")


app.register("ready", on_ready)
