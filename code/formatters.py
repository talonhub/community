from talon import Module, Context, actions, ui, imgui
from talon.grammar import Phrase
from typing import List, Union

ctx = Context()
key = actions.key

words_to_keep_lowercase = "a,an,the,at,by,for,in,is,of,on,to,up,and,as,but,or,nor".split(
    ","
)

last_formatted_phrase = ""
last_phrase = ""


def surround(by):
    def func(i, word, last):
        if i == 0:
            word = by + word
        if last:
            word += by
        return word

    return func


def FormatText(m: Union[str, Phrase], fmtrs: str):
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

    return format_text_helper(words, fmtrs)


def format_text_helper(word_list, fmtrs: str):
    fmtr_list = fmtrs.split(",")
    tmp = []
    spaces = True
    for i, w in enumerate(word_list):
        for name in reversed(fmtr_list):
            smash, func = all_formatters[name]
            w = func(i, w, i == len(word_list) - 1)
            spaces = spaces and not smash
        tmp.append(w)
    words = tmp

    sep = " "
    if not spaces:
        sep = ""
    result = sep.join(words)

    global last_formatted_phrase
    last_formatted_phrase = result
    return result


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
    "DOUBLE_COLON_SEPARATED": words_with_joiner("::"),
    "ALL_CAPS": (SEP, every_word(lambda w: w.upper())),
    "ALL_LOWERCASE": (SEP, every_word(lambda w: w.lower())),
    "DOUBLE_QUOTED_STRING": (SEP, surround('"')),
    "SINGLE_QUOTED_STRING": (SEP, surround("'")),
    "SPACE_SURROUNDED_STRING": (SEP, surround(" ")),
    "DOT_SEPARATED": words_with_joiner("."),
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
    "say": formatters_dict["NOOP"],
    "sentence": formatters_dict["CAPITALIZE_FIRST_WORD"],
    "slasher": formatters_dict["SLASH_SEPARATED"],
    "smash": formatters_dict["NO_SPACES"],
    "snake": formatters_dict["SNAKE_CASE"],
    "speak": formatters_dict["NOOP"],
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
        return FormatText(phrase, formatters)

    def list_formatters():
        """Lists all formatters"""
        gui.freeze()

    def hide_formatters():
        """Hides list of formatters"""
        gui.hide()

    def clear_last_phrase():
        """Clears the last formatted phrase"""
        global last_formatted_phrase
        for character in last_formatted_phrase:
            actions.edit.delete()

    def reformat_last_phrase(formatters: str) -> str:
        """Reformats last formatted phrase"""
        global last_phrase
        return FormatText(last_phrase, formatters)


@ctx.capture(rule="{self.formatters}+")
def formatters(m):
    return ",".join(m.formatters_list)


@ctx.capture(rule="<self.formatters> <user.text>")
def format_text(m):
    return FormatText(m.text, m.formatters)


ctx.lists["self.formatters"] = formatters_words.keys()


@imgui.open(software=False)
def gui(gui: imgui.GUI):
    gui.text("List formatters")
    gui.line()
    for name in sorted(set(formatters_words.keys())):
        gui.text(f"{name} | {format_text_helper(['one', 'two', 'three'], name)}")
