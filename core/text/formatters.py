import logging
import re
from typing import Union

from talon import Context, Module, actions, app
from talon.grammar import Phrase

ctx = Context()
key = actions.key
edit = actions.edit

words_to_keep_lowercase = (
    "a an and as at but by en for if in nor of on or per the to v via vs".split()
)

# The last phrase spoken, without & with formatting. Used for reformatting.
last_phrase = ""
last_phrase_formatted = ""

# Internally, a formatter is a pair (sep, fn).
#
# - sep: a boolean, true iff the formatter should leave spaces between words.
#   We use SEP & NOSEP for this for clarity.
#
# - fn: a function (i, word, is_end) --> formatted_word, called on each `word`.
#   `i` is the word's index in the list, and `is_end` is True iff it's the
#   last word in the list.
SEP = True
NOSEP = False


def format_phrase(m: Union[str, Phrase], formatters: str):
    global last_phrase, last_phrase_formatted
    last_phrase = m
    words = []
    if isinstance(m, str):
        words = m.split(" ")
    else:
        # # I believe this is no longer necessary. -rntz, 2022-02-10
        # # TODO: I've commented this out, remove if nobody has issues -rntz, 2022-06-21
        # if m.words[-1] == "over":
        #     m.words = m.words[:-1]
        words = actions.dictate.replace_words(actions.dictate.parse_words(m))

    result = last_phrase_formatted = format_phrase_without_adding_to_history(
        words, formatters
    )
    actions.user.add_phrase_to_history(result)
    # Arguably, we shouldn't be dealing with history here, but somewhere later
    # down the line. But we have a bunch of code that relies on doing it this
    # way and I don't feel like rewriting it just now. -rntz, 2020-11-04
    return result


def format_phrase_without_adding_to_history(word_list, formatters: str):
    # A formatter is a pair (keep_spaces, function). We drop spaces if any
    # formatter does; we apply their functions in reverse order.
    formatters = [all_formatters[name] for name in formatters.split(",")]
    separator = " " if all(x[0] for x in formatters) else ""
    functions = [x[1] for x in reversed(formatters)]
    words = []
    for i, word in enumerate(word_list):
        for f in functions:
            word = f(i, word, i == len(word_list) - 1)
        words.append(word)
    return separator.join(words)


# Formatter helpers
def surround(by):
    return lambda i, word, last: (by if i == 0 else "") + word + (by if last else "")


def words_with_joiner(joiner):
    """Pass through words unchanged, but add a separator between them."""
    return (NOSEP, lambda i, word, _: ("" if i == 0 else joiner) + word)


def first_vs_rest(first_func, rest_func=lambda w: w):
    """Supply one or two transformer functions for the first and rest of
    words respectively.

    Leave second argument out if you want all but the first word to be passed
    through unchanged.
    Set first argument to None if you want the first word to be passed
    through unchanged.
    """
    first_func = first_func or (lambda w: w)
    return lambda i, word, _: first_func(word) if i == 0 else rest_func(word)


def title_case():
    last_word = None

    def title_case_word(i, word, is_end):
        nonlocal last_word

        if word.islower() and (  # contains only lowercase letters
            word not in words_to_keep_lowercase
            or i == 0
            or is_end
            or not last_word[
                -1
            ].isalnum()  # title case subsequent words if they follow punctuation
        ):
            if "-" in word:
                components = word.split("-")
                title_case_component = title_case()
                components = [
                    title_case_component(j, component, j == len(components) - 1)
                    for j, component in enumerate(components)
                ]
                word = "-".join(components)
            elif word_start := re.match(r"\W*", word).end():
                # word begins with non-alphanumeric characters
                word = word[:word_start] + word[word_start:].capitalize()
            else:
                word = word.capitalize()

        last_word = word

        return word

    return title_case_word


def every_word(word_func):
    """Apply one function to every word."""
    return lambda i, word, _: word_func(word)


# All formatters (code and prose)
formatters_dict = {
    "NOOP": (SEP, lambda i, word, _: word),
    "DOUBLE_UNDERSCORE": (NOSEP, first_vs_rest(lambda w: f"__{w}__")),
    "PRIVATE_CAMEL_CASE": (
        NOSEP,
        first_vs_rest(lambda w: w.lower(), lambda w: w.capitalize()),
    ),
    "PROTECTED_CAMEL_CASE": (
        NOSEP,
        first_vs_rest(lambda w: w.lower(), lambda w: w.capitalize()),
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
    "CAPITALIZE_FIRST_WORD": (
        SEP,
        first_vs_rest(lambda w: title_case()(0, w, True)),
    ),
    "CAPITALIZE_ALL_WORDS": (SEP, title_case()),
}

# Mapping from spoken phrases to formatter names
code_formatter_names = {
    "all cap":"ALL_CAPS",
    "all down": "ALL_LOWERCASE",
    "camel": "PRIVATE_CAMEL_CASE",
    "dotted": "DOT_SEPARATED",
    "dub string": "DOUBLE_QUOTED_STRING",
    "dunder": "DOUBLE_UNDERSCORE",
    "hammer": "PUBLIC_CAMEL_CASE",
    "kebab": "DASH_SEPARATED",
    "dasher": "DASH_SEPARATED",
    "packed": "DOUBLE_COLON_SEPARATED",
    "padded": "SPACE_SURROUNDED_STRING",
    "slasher": "SLASH_SEPARATED",
    "smash": "NO_SPACES",
    "snake": "SNAKE_CASE",
    "string": "SINGLE_QUOTED_STRING",
    "title": "CAPITALIZE_ALL_WORDS",
    "proud": "CAPITALIZE_ALL_WORDS",
}
prose_formatter_names = {
    # "say": "NOOP",
    "speak": "NOOP",
    "sentence": "CAPITALIZE_FIRST_WORD",
}
# Mapping from spoken phrases to formatters
formatter_words = {
    phrase: formatters_dict[name]
    for phrase, name in (code_formatter_names | prose_formatter_names).items()
}

# Allow referencing formatters by either their names or spoken forms
all_prose_formatters = [
    item for sublist in prose_formatter_names.items() for item in sublist
]
all_formatters = formatters_dict | formatter_words

mod = Module()
mod.list("formatters", desc="list of all formatters (code and prose)")
mod.list("code_formatter", desc="list of formatters typically applied to code")
mod.list(
    "prose_formatter", desc="list of prose formatters (words to start dictating prose)"
)


@mod.capture(rule="{self.formatters}+")
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m.formatters_list)


@mod.capture(rule="{self.code_formatter}+")
def code_formatters(m) -> str:
    "Returns a comma-separated string of code formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m.code_formatter_list)


@mod.capture(
    # Note that if the user speaks something like "snake dot", it will
    # insert "dot" - otherwise, they wouldn't be able to insert punctuation
    # words directly.
    rule="<self.formatters> <user.text> (<user.text> | <user.formatter_immune>)*"
)
def format_text(m) -> str:
    """Formats text and returns a string"""
    out = ""
    formatters = m[0]
    for chunk in m[1:]:
        if isinstance(chunk, ImmuneString):
            out += chunk.string
        else:
            out += format_phrase(chunk, formatters)
    return out


@mod.capture(
    rule="<self.code_formatters> <user.text> (<user.text> | <user.formatter_immune>)*"
)
def format_code(m) -> str:
    """Formats code and returns a string"""
    return format_text(m)


class ImmuneString:
    """Wrapper that makes a string immune from formatting."""

    def __init__(self, string):
        self.string = string


@mod.capture(
    # Add anything else into this that you want to be able to speak during a
    # formatter.
    rule="(<user.symbol_key> | (numb | numeral) <number>)"
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

    def insert_with_history(text: str):
        """Inserts some text, remembering it in the phrase history."""
        actions.user.deprecate_action("2022-12-11", "user.insert_with_history")

        actions.user.add_phrase_to_history(text)
        actions.insert(text)

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
        if not selected:
            app.notify("Asked to reformat selection, but nothing selected!")
            return
        if formatters not in all_prose_formatters:
            selected = unformat_text(selected)
        # Delete separately for compatibility with programs that don't overwrite
        # selected text (e.g. Emacs)
        edit.delete()
        text = actions.self.formatted_text(selected, formatters)
        actions.insert(text)
        return text

    def get_formatters_words() -> dict:
        """returns a list of words currently used as formatters, and a demonstration string using those formatters"""
        formatters_help_demo = {}
        for name in sorted(set(formatter_words)):
            demo = format_phrase_without_adding_to_history(
                ["one", "two", "three"], name
            )
            if name in prose_formatter_names:
                name += " *"
            formatters_help_demo[name] = demo
        return formatters_help_demo

    def reformat_text(text: str, formatters: str) -> str:
        """Reformat the text."""
        if formatters not in all_prose_formatters:
            text = unformat_text(text)
        return actions.user.formatted_text(text, formatters)

    def insert_many(strings: list[str]) -> None:
        """Insert a list of strings, sequentially."""
        for string in strings:
            actions.insert(string)


def unformat_text(text: str) -> str:
    """Remove format from text"""
    unformatted = re.sub(r"[\W_]+", " ", text)
    # Split on camelCase, including numbers
    # FIXME: handle non-ASCII letters!
    unformatted = re.sub(
        r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])",
        " ",
        unformatted,
    )
    # TODO: Separate out studleycase vars
    return unformatted.lower()


ctx.lists["self.formatters"] = formatter_words.keys()
ctx.lists["self.code_formatter"] = code_formatter_names.keys()
ctx.lists["self.prose_formatter"] = prose_formatter_names.keys()
