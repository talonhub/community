from talon import Module, Context, actions, ui, imgui
from talon.grammar import Phrase
from typing import List, Union

ctx = Context()
key = actions.key

words_to_keep_lowercase = "a,an,the,at,by,for,in,is,of,on,to,up,and,as,but,or,nor".split(
    ","
)

# last_phrase has the last phrase spoken, WITHOUT formatting.
# This is needed for reformatting.
last_phrase = ""

# formatted_phrase_history keeps the most recent formatted phrases, WITH formatting.
formatted_phrase_history = []
formatted_phrase_history_length = 20


def surround(by):
    def func(i, word, last):
        if i == 0:
            word = by + word
        if last:
            word += by
        return word

    return func


def format_phrase(m: Union[str, Phrase], fmtrs: str):
    global last_phrase
    last_phrase = m
    words = []
    if isinstance(m, str):
        words = m.split(" ")
    else:
        if m.words[-1] == "over":
            m.words = m.words[:-1]

        words = actions.dictate.parse_words(m)
        words = actions.dictate.replace_words(words)

    result = format_phrase_no_history(words, fmtrs)

    # Add result to history.
    global formatted_phrase_history
    formatted_phrase_history.insert(0, result)
    formatted_phrase_history = formatted_phrase_history[
        :formatted_phrase_history_length
    ]

    return result


def format_phrase_no_history(word_list, fmtrs: str):
    fmtr_list = fmtrs.split(",")
    words = []
    spaces = True
    for i, w in enumerate(word_list):
        for name in reversed(fmtr_list):
            smash, func = all_formatters[name]
            w = func(i, w, i == len(word_list) - 1)
            spaces = spaces and not smash
        words.append(w)
    sep = " " if spaces else ""
    return sep.join(words)


NOSEP = True
SEP = False


def words_with_joiner(joiner):
    """Pass through words unchanged, but add a separator between them."""

    def formatter_function(i, word, _):
        return word if i == 0 else joiner + word

    return (NOSEP, formatter_function)


def first_vs_rest(first_func, rest_func=lambda w: w):
    """Supply one or two transformer functions for the first and rest of
    words respectively.

    Leave second argument out if you want all but the first word to be passed
    through unchanged.
    Set first argument to None if you want the first word to be passed
    through unchanged."""
    if first_func is None:
        first_func = lambda w: w

    def formatter_function(i, word, _):
        return first_func(word) if i == 0 else rest_func(word)

    return formatter_function


def every_word(word_func):
    """Apply one function to every word."""

    def formatter_function(i, word, _):
        return word_func(word)

    return formatter_function


formatters_dict = {
    "NOOP": (SEP, lambda i, word, _: word),
    "DOUBLE_UNDERSCORE": (NOSEP, first_vs_rest(lambda w: "__%s__" % w)),
    "PRIVATE_CAMEL_CASE": (NOSEP, first_vs_rest(lambda w: w, lambda w: w.capitalize())),
    "PROTECTED_CAMEL_CASE": (
        NOSEP,
        first_vs_rest(lambda w: w, lambda w: w.capitalize()),
    ),
    "PUBLIC_CAMEL_CASE": (NOSEP, every_word(lambda w: w.capitalize())),
    "SNAKE_CASE": (
        NOSEP,
        first_vs_rest(lambda w: w.lower(), lambda w: "_" + w.lower()),
    ),
    "NO_SPACES": (NOSEP, every_word(lambda w: w)),
    "DASH_SEPARATED": words_with_joiner("-"),
    "TERMINAL_DASH_SEPARATED": (
        NOSEP,
        first_vs_rest(lambda w: " --" + w.lower(), lambda w: "-" + w.lower()),
    ),
    "DOUBLE_COLON_SEPARATED": words_with_joiner("::"),
    "ALL_CAPS": (SEP, every_word(lambda w: w.upper())),
    "ALL_LOWERCASE": (SEP, every_word(lambda w: w.lower())),
    "DOUBLE_QUOTED_STRING": (SEP, surround('"')),
    "SINGLE_QUOTED_STRING": (SEP, surround("'")),
    "SPACE_SURROUNDED_STRING": (SEP, surround(" ")),
    "DOT_SEPARATED": words_with_joiner("."),
    "DOT_SNAKE": (NOSEP, lambda i, word, _: "." + word if i == 0 else "_" + word),
    "SLASH_SEPARATED": (NOSEP, every_word(lambda w: "/" + w)),
    "CAPITALIZE_FIRST_WORD": (SEP, first_vs_rest(lambda w: w.capitalize())),
    "CAPITALIZE_ALL_WORDS": (
        SEP,
        lambda i, word, _: word.capitalize()
        if i == 0 or word not in words_to_keep_lowercase
        else word,
    ),
    "FIRST_THREE": (NOSEP, lambda i, word, _: word[0:3]),
    "FIRST_FOUR": (NOSEP, lambda i, word, _: word[0:4]),
    "FIRST_FIVE": (NOSEP, lambda i, word, _: word[0:5]),
}

# This is the mapping from spoken phrases to formatters
formatters_words = {
    "allcaps": formatters_dict["ALL_CAPS"],
    "alldown": formatters_dict["ALL_LOWERCASE"],
    "camel": formatters_dict["PRIVATE_CAMEL_CASE"],
    "dotted": formatters_dict["DOT_SEPARATED"],
    "dubstring": formatters_dict["DOUBLE_QUOTED_STRING"],
    "dunder": formatters_dict["DOUBLE_UNDERSCORE"],
    "hammer": formatters_dict["PUBLIC_CAMEL_CASE"],
    "kebab": formatters_dict["DASH_SEPARATED"],
    "packed": formatters_dict["DOUBLE_COLON_SEPARATED"],
    "padded": formatters_dict["SPACE_SURROUNDED_STRING"],
    # "say": formatters_dict["NOOP"],
    "sentence": formatters_dict["CAPITALIZE_FIRST_WORD"],
    "slasher": formatters_dict["SLASH_SEPARATED"],
    "smash": formatters_dict["NO_SPACES"],
    "snake": formatters_dict["SNAKE_CASE"],
    # "speak": formatters_dict["NOOP"],
    "string": formatters_dict["SINGLE_QUOTED_STRING"],
    "title": formatters_dict["CAPITALIZE_ALL_WORDS"],
    # disable a few formatters for now
    # "tree": formatters_dict["FIRST_THREE"],
    # "quad": formatters_dict["FIRST_FOUR"],
    # "fiver": formatters_dict["FIRST_FIVE"],
}

all_formatters = {}
all_formatters.update(formatters_dict)
all_formatters.update(formatters_words)

mod = Module()
mod.list("formatters", desc="list of formatters")


@mod.capture
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"


@mod.capture
def format_text(m) -> str:
    "Formats the text and returns a string"


@mod.action_class
class Actions:
    def formatted_text(phrase: Union[str, Phrase], formatters: str) -> str:
        """Formats a phrase according to formatters. formatters is a comma-separated string of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        return format_phrase(phrase, formatters)

    def formatters_help_toggle():
        """Lists all formatters"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def formatters_recent_toggle():
        """Toggles list of recent formatters"""
        if recent_gui.showing:
            recent_gui.hide()
        else:
            recent_gui.show()

    def formatters_recent_select(number: int):
        """Inserts a recent formatter"""
        if len(formatted_phrase_history) >= number:
            return formatted_phrase_history[number - 1]
        return ""

    def formatters_clear_last():
        """Clears the last formatted phrase"""
        if len(formatted_phrase_history) > 0:
            for character in formatted_phrase_history[0]:
                actions.edit.delete()

    def formatters_reformat_last(formatters: str) -> str:
        """Reformats last formatted phrase"""
        global last_phrase
        return format_phrase(last_phrase, formatters)


@ctx.capture(rule="{self.formatters}+")
def formatters(m):
    return ",".join(m.formatters_list)


@ctx.capture(rule="<self.formatters> <user.text>")
def format_text(m):
    return format_phrase(m.text, m.formatters)


ctx.lists["self.formatters"] = formatters_words.keys()


@imgui.open(software=False)
def gui(gui: imgui.GUI):
    gui.text("List formatters")
    gui.line()
    for name in sorted(set(formatters_words.keys())):
        gui.text(f"{name} | {format_phrase_no_history(['one', 'two', 'three'], name)}")


@imgui.open(software=False)
def recent_gui(gui: imgui.GUI):
    gui.text("Recent formatters")
    gui.line()
    for index, result in enumerate(formatted_phrase_history, 1):
        gui.text("{}. {}".format(index, result))
