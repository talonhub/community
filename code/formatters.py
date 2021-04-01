from talon import Module, Context, actions, ui, imgui, app
from talon.grammar import Phrase
from typing import List, Union
import logging
import re

ctx = Context()
key = actions.key
edit = actions.edit

words_to_keep_lowercase = "a,an,the,at,by,for,in,is,of,on,to,up,and,as,but,or,nor".split(
    ","
)

# The last phrase spoken, without & with formatting. Used for reformatting.
last_phrase = ""
last_phrase_formatted = ""


def surround(by):
    def func(i, word, last):
        if i == 0:
            word = by + word
        if last:
            word += by
        return word

    return func


def format_phrase(m: Union[str, Phrase], fmtrs: str):
    global last_phrase, last_phrase_formatted
    last_phrase = m
    words = []
    if isinstance(m, str):
        words = m.split(" ")
    else:
        # TODO: is this still necessary, and if so why?
        if m.words[-1] == "over":
            m.words = m.words[:-1]

        words = actions.dictate.parse_words(m)
        words = actions.dictate.replace_words(words)

    result = last_phrase_formatted = format_phrase_no_history(words, fmtrs)
    actions.user.add_phrase_to_history(result)
    # Arguably, we shouldn't be dealing with history here, but somewhere later
    # down the line. But we have a bunch of code that relies on doing it this
    # way and I don't feel like rewriting it just now. -rntz, 2020-11-04
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
    # "sentence": formatters_dict["CAPITALIZE_FIRST_WORD"],
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
mod.list(
    "prose_formatter",
    desc="words to start dictating prose, and the formatter they apply",
)


@mod.capture(rule="{self.formatters}+")
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m.formatters_list)


@mod.capture(
    # Note that if the user speaks something like "snake dot", it will
    # insert "dot" - otherwise, they wouldn't be able to insert punctuation
    # words directly.
    rule="<self.formatters> <user.text> (<user.text> | <user.formatter_immune>)*"
)
def format_text(m) -> str:
    "Formats the text and returns a string"
    out = ""
    formatters = m[0]
    for chunk in m[1:]:
        if isinstance(chunk, ImmuneString):
            out += chunk.string
        else:
            out += format_phrase(chunk, formatters)
    return out


class ImmuneString(object):
    """Wrapper that makes a string immune from formatting."""

    def __init__(self, string):
        self.string = string


@mod.capture(
    # Add anything else into this that you want to be able to speak during a
    # formatter.
    rule="(<user.symbol_key> | numb <number>)"
)
def formatter_immune(m) -> ImmuneString:
    """Text that can be interspersed into a formatter, e.g. characters.

    It will be inserted directly, without being formatted.

    """
    if hasattr(m, "number"):
        value = m.number
    else:
        value = m[0]
    return ImmuneString(str(value))


@mod.action_class
class Actions:
    def formatted_text(phrase: Union[str, Phrase], formatters: str) -> str:
        """Formats a phrase according to formatters. formatters is a comma-separated string of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        return format_phrase(phrase, formatters)

    def insert_formatted(phrase: Union[str, Phrase], formatters: str):
        """Inserts a phrase formatted according to formatters. Formatters is a comma separated list of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        actions.insert(format_phrase(phrase, formatters))

    def formatters_help_toggle():
        """Lists all formatters"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def formatters_reformat_last(formatters: str) -> str:
        """Clears and reformats last formatted phrase"""
        global last_phrase, last_phrase_formatted
        if actions.user.get_last_phrase() != last_phrase_formatted:
            # The last thing we inserted isn't the same as the last thing we
            # formatted, so abort.
            logging.warning(
                "formatters_reformat_last(): Last phrase wasn't a formatter!"
            )
            return
        actions.user.clear_last_phrase()
        actions.user.insert_formatted(last_phrase, formatters)

    def formatters_reformat_selection(formatters: str) -> str:
        """Reformats the current selection."""
        selected = edit.selected_text()
        unformatted = re.sub(r"[^a-zA-Z0-9]+", " ", selected).lower()
        # TODO: Separate out camelcase & studleycase vars

        # Delete separately for compatibility with programs that don't overwrite
        # selected text (e.g. Emacs)
        edit.delete()
        text = actions.self.formatted_text(unformatted, formatters)
        actions.insert(text)
        return text

    def insert_many(strings: List[str]) -> None:
        """Insert a list of strings, sequentially."""
        for string in strings:
            actions.insert(string)


ctx.lists["self.formatters"] = formatters_words.keys()
ctx.lists["self.prose_formatter"] = {
    "say": "NOOP",
    "speak": "NOOP",
    "sentence": "CAPITALIZE_FIRST_WORD",
}


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("List formatters")
    gui.line()
    for name in sorted(set(formatters_words.keys())):
        gui.text(f"{name} | {format_phrase_no_history(['one', 'two', 'three'], name)}")
