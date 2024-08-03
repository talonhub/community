import logging
import re
from abc import ABC, abstractmethod
from typing import Callable, Optional, Union

from talon import Context, Module, actions, app
from talon.grammar import Phrase


class Formatter(ABC):
    def __init__(self, id: str):
        self.id = id

    @abstractmethod
    def format(self, text: str) -> str:
        pass

    @abstractmethod
    def unformat(self, text: str) -> str:
        pass


class CustomFormatter(Formatter):
    def __init__(
        self,
        id: str,
        format: Callable[[str], str],
        unformat: Optional[Callable[[str], str]] = None,
    ):
        super().__init__(id)
        self._format = format
        self._unformat = unformat

    def format(self, text: str) -> str:
        return self._format(text)

    def unformat(self, text: str) -> str:
        if self._unformat:
            return self._unformat(text)
        return text


class CodeFormatter(Formatter):
    def __init__(
        self,
        id: str,
        delimiter: str,
        format_first: Callable[[str], str],
        format_rest: Callable[[str], str],
    ):
        super().__init__(id)
        self._delimiter = delimiter
        self._format_first = format_first
        self._format_rest = format_rest

    def format(self, text: str) -> str:
        return self._format_delim(
            text, self._delimiter, self._format_first, self._format_rest
        )

    def unformat(self, text: str) -> str:
        return remove_code_formatting(text)

    def _format_delim(
        self,
        text: str,
        delimiter: str,
        format_first: Callable[[str], str],
        format_rest: Callable[[str], str],
    ):
        # Strip anything that is not alpha-num, whitespace, dot or comma
        text = re.sub(r"[^\w\d\s.,]+", "", text)
        # Split on anything that is not alpha-num
        words = re.split(r"([^\w\d]+)", text)
        groups = []
        group = []
        first = True

        for word in words:
            if word.isspace():
                continue
            # Word is number
            if word.isnumeric():
                first = True
            # Word is symbol
            elif not word.isalpha():
                groups.append(delimiter.join(group))
                word = word.strip()
                if word != ".":
                    word += " "
                first = True
                groups.append(word)
                group = []
                continue
            elif first:
                first = False
                if format_first:
                    word = format_first(word)
            elif format_rest:
                word = format_rest(word)
            group.append(word)

        groups.append(delimiter.join(group))
        return "".join(groups)


class TitleFormatter(Formatter):
    _words_to_keep_lowercase = (
        "a an and as at but by en for if in nor of on or per the to v via vs".split()
    )

    def format(self, text: str) -> str:
        words = [x for x in re.split(r"(\s+)", text) if x]
        words = self._title_case_words(words)
        return "".join(words)

    def unformat(self, text: str) -> str:
        return unformat_upper(text)

    def _title_case_word(
        self, word: str, is_first: bool, is_last: bool, following_symbol: bool
    ) -> str:
        if not word.islower() or (
            word in self._words_to_keep_lowercase
            and not is_first
            and not is_last
            and not following_symbol
        ):
            return word

        if "-" in word:
            words = word.split("-")
            words = self._title_case_words(words)
            return "-".join(words)

        return word.capitalize()

    def _title_case_words(self, words: list[str]) -> list[str]:
        following_symbol = False
        for i, word in enumerate(words):
            if word.isspace():
                continue
            is_first = i == 0
            is_last = i == len(words) - 1
            words[i] = self._title_case_word(word, is_first, is_last, following_symbol)
            following_symbol = not word[-1].isalnum()
        return words


class CapitalizeFormatter(Formatter):
    def format(self, text: str) -> str:
        return re.sub(r"^\S+", lambda m: capitalize_first(m.group()), text)

    def unformat(self, text: str) -> str:
        return unformat_upper(text)


class SentenceFormatter(Formatter):
    def format(self, text: str) -> str:
        """Capitalize first word if it's already all lower case"""
        words = [x for x in re.split(r"(\s+)", text) if x]
        if words and words[0].islower():
            words[0] = words[0].capitalize()
        return "".join(words)

    def unformat(self, text: str) -> str:
        return unformat_upper(text)


def capitalize_first(text: str) -> str:
    return text[:1].upper() + text[1:]


def capitalize(text: str) -> str:
    return text.capitalize()


def lower(text: str) -> str:
    return text.lower()


def unformat_upper(text: str) -> str:
    return text.lower() if text.isupper() else text


def remove_code_formatting(text: str) -> str:
    """Remove format from text"""
    # Split on delimiters.
    result = re.sub(r"[-_.:/]+", " ", text)
    # Split camel case. Including numbers
    result = de_camel(result)
    # Delimiter/camel case successfully split. Lower case to restore "original" text.
    if text != result:
        return result.lower()
    return text


def de_camel(text: str) -> str:
    """Replacing camelCase boundaries with blank space"""
    Ll = "a-zåäö"
    Lu = "A-ZÅÄÖ"
    L = f"{Ll}{Lu}"
    low_to_upper = rf"(?<=[{Ll}])(?=[{Lu}])"  # camel|Case
    upper_to_last_upper = rf"(?<=[L{Lu}])(?=[{Lu}][{Ll}])"  # IP|Address
    letter_to_digit = rf"(?<=[{L}])(?=[\d])"  # version|10
    digit_to_letter = rf"(?<=[\d])(?=[{L}])"  # 2|x
    return re.sub(
        rf"{low_to_upper}|{upper_to_last_upper}|{letter_to_digit}|{digit_to_letter}",
        " ",
        text,
    )


formatter_list = [
    CustomFormatter("NOOP", lambda text: text),
    CustomFormatter("TRAILING_SPACE", lambda text: f"{text} "),
    CustomFormatter("DOUBLE_QUOTED_STRING", lambda text: f'"{text}"'),
    CustomFormatter("SINGLE_QUOTED_STRING", lambda text: f"'{text}'"),
    CustomFormatter("SPACE_SURROUNDED_STRING", lambda text: f" {text} "),
    CustomFormatter("ALL_CAPS", lambda text: text.upper()),
    CustomFormatter("ALL_LOWERCASE", lambda text: text.lower()),
    CustomFormatter("COMMA_SEPARATED", lambda text: re.sub(r"\s+", ", ", text)),
    CustomFormatter("REMOVE_FORMATTING", remove_code_formatting),
    TitleFormatter("CAPITALIZE_ALL_WORDS"),
    # The sentence formatter being called `CAPITALIZE_FIRST_WORD` is a bit of a misnomer, but kept for backward compatibility.
    SentenceFormatter("CAPITALIZE_FIRST_WORD"),
    # This is the formatter that actually just capitalizes the first word
    CapitalizeFormatter("CAPITALIZE"),
    CodeFormatter("NO_SPACES", "", lower, lower),
    CodeFormatter("PRIVATE_CAMEL_CASE", "", lower, capitalize),
    CodeFormatter("PUBLIC_CAMEL_CASE", "", capitalize, capitalize),
    CodeFormatter("SNAKE_CASE", "_", lower, lower),
    CodeFormatter("DASH_SEPARATED", "-", lower, lower),
    CodeFormatter("DOT_SEPARATED", ".", lower, lower),
    CodeFormatter("SLASH_SEPARATED", "/", lower, lower),
    CodeFormatter("ALL_SLASHES", "/", lambda text: f"/{text.lower()}", lower),
    CodeFormatter("DOUBLE_UNDERSCORE", "__", lower, lower),
    CodeFormatter("DOUBLE_COLON_SEPARATED", "::", lower, lower),
]

formatters_dict = {f.id: f for f in formatter_list}


# Mapping from spoken phrases to formatter names
code_formatter_names = {
    "all cap": "ALL_CAPS",
    "all down": "ALL_LOWERCASE",
    "camel": "PRIVATE_CAMEL_CASE",
    "dotted": "DOT_SEPARATED",
    "dub string": "DOUBLE_QUOTED_STRING",
    "dunder": "DOUBLE_UNDERSCORE",
    "hammer": "PUBLIC_CAMEL_CASE",
    "kebab": "DASH_SEPARATED",
    "packed": "DOUBLE_COLON_SEPARATED",
    "padded": "SPACE_SURROUNDED_STRING",
    "slasher": "ALL_SLASHES",
    "conga": "SLASH_SEPARATED",
    "smash": "NO_SPACES",
    "snake": "SNAKE_CASE",
    "string": "SINGLE_QUOTED_STRING",
    "constant": "ALL_CAPS,SNAKE_CASE",
}
prose_formatter_names = {
    "say": "NOOP",
    "speak": "NOOP",
    "sentence": "CAPITALIZE_FIRST_WORD",
    "title": "CAPITALIZE_ALL_WORDS",
}
reformatter_names = {
    "cap": "CAPITALIZE",
    "list": "COMMA_SEPARATED",
    "unformat": "REMOVE_FORMATTING",
}
word_formatter_names = {
    "word": "ALL_LOWERCASE",
    "trot": "TRAILING_SPACE,ALL_LOWERCASE",
    "proud": "CAPITALIZE_FIRST_WORD",
    "leap": "TRAILING_SPACE,CAPITALIZE_FIRST_WORD",
}


all_phrase_formatters = code_formatter_names | prose_formatter_names | reformatter_names

mod = Module()
mod.list("formatters", desc="list of all formatters (code and prose)")
mod.list("code_formatter", desc="list of formatters typically applied to code")
mod.list(
    "prose_formatter", desc="list of prose formatters (words to start dictating prose)"
)
mod.list("word_formatter", "List of word formatters")

ctx = Context()
ctx.lists["self.formatters"] = all_phrase_formatters
ctx.lists["self.code_formatter"] = code_formatter_names
ctx.lists["self.prose_formatter"] = prose_formatter_names
ctx.lists["user.word_formatter"] = word_formatter_names


# The last phrase spoken, without & with formatting. Used for reformatting.
last_phrase = ""
last_phrase_formatted = ""


def format_phrase(
    m: Union[str, Phrase], formatters: str, unformat: bool = False
) -> str:
    global last_phrase, last_phrase_formatted
    last_phrase = m

    if isinstance(m, str):
        text = m
    else:
        text = " ".join(actions.dictate.replace_words(actions.dictate.parse_words(m)))

    result = last_phrase_formatted = format_text_without_adding_to_history(
        text, formatters, unformat
    )

    actions.user.add_phrase_to_history(result)
    # Arguably, we shouldn't be dealing with history here, but somewhere later
    # down the line. But we have a bunch of code that relies on doing it this
    # way and I don't feel like rewriting it just now. -rntz, 2020-11-04
    return result


def format_text_without_adding_to_history(
    text: str, formatters: str, unformat: bool = False
) -> str:
    """Formats a text according to formatters. formatters is a comma-separated string of formatters (e.g. 'TITLE_CASE,SNAKE_CASE')"""
    if not text:
        return text

    text, pre, post = shrink_to_string_inside(text)

    for i, formatter_name in enumerate(reversed(formatters.split(","))):
        formatter = formatters_dict[formatter_name]
        if unformat and i == 0:
            text = formatter.unformat(text)
        text = formatter.format(text)

    return f"{pre}{text}{post}"


string_delimiters = [
    ['"""', '"""'],
    ['"', '"'],
    ["'", "'"],
]


def shrink_to_string_inside(text: str) -> tuple[str, str, str]:
    for [left, right] in string_delimiters:
        if text.startswith(left) and text.endswith(right):
            return text[len(left) : -len(right)], left, right
    return text, "", ""


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

    def formatters_reformat_last(formatters: str):
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

    def reformat_text(text: str, formatters: str) -> str:
        """Re-formats <text> as <formatters>"""
        return format_phrase(text, formatters, True)

    def formatters_reformat_selection(formatters: str):
        """Reformats the current selection as <formatters>"""
        selected = actions.edit.selected_text()
        if not selected:
            app.notify("Asked to reformat selection, but nothing selected!")
            return
        # Delete separately for compatibility with programs that don't overwrite
        # selected text (e.g. Emacs)
        actions.edit.delete()
        text = actions.user.reformat_text(selected, formatters)
        actions.insert(text)

    def get_formatters_words() -> dict:
        """Returns words currently used as formatters, and a demonstration string using those formatters"""
        formatters_help_demo = {}
        for phrase in sorted(all_phrase_formatters):
            name = all_phrase_formatters[phrase]
            demo = format_text_without_adding_to_history("one two three", name)
            if phrase in prose_formatter_names:
                phrase += " *"
            formatters_help_demo[phrase] = demo
        return formatters_help_demo

    def get_reformatters_words() -> dict:
        """Returns words currently used as re-formatters, and a demonstration string using those re-formatters"""
        formatters_help_demo = {}
        for phrase in sorted(all_phrase_formatters):
            name = all_phrase_formatters[phrase]
            demo = format_text_without_adding_to_history("one_two_three", name, True)
            if phrase in prose_formatter_names:
                phrase += " *"
            formatters_help_demo[phrase] = demo
        return formatters_help_demo

    def insert_many(strings: list[str]) -> None:
        """Insert a list of strings, sequentially."""
        for string in strings:
            actions.insert(string)
