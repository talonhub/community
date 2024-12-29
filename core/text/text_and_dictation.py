# Descended from https://github.com/dwiel/talon_community/blob/master/misc/dictation.py
import re
from typing import Callable, Optional

from talon import Context, Module, actions, grammar, settings, ui

from ..numbers.numbers import get_spoken_form_under_one_hundred

mod = Module()

mod.setting(
    "context_sensitive_dictation",
    type=bool,
    default=False,
    desc="Look at surrounding text to improve auto-capitalization/spacing in dictation mode. By default, this works by selecting that text & copying it to the clipboard, so it may be slow or fail in some applications.",
)

mod.list("prose_modifiers", desc="Modifiers that can be used within prose")
mod.list("prose_snippets", desc="Snippets that can be used within prose")
mod.list("phrase_ender", "List of commands that can be used to end a phrase")
mod.list("hours_twelve", desc="Names for hours up to 12")
mod.list("hours", desc="Names for hours up to 24")
mod.list("minutes", desc="Names for minutes, 01 up to 59")
mod.list(
    "currency",
    desc="Currency types (e.g., dollars, euros) that can be used within prose",
)

ctx = Context()
ctx_dragon = Context()
ctx_dragon.matches = r"""
speech.engine: dragon
"""

ctx.lists["user.hours_twelve"] = get_spoken_form_under_one_hundred(
    1,
    12,
    include_oh_variant_for_single_digits=True,
    include_default_variant_for_single_digits=True,
)
ctx.lists["user.hours"] = get_spoken_form_under_one_hundred(
    1,
    23,
    include_oh_variant_for_single_digits=True,
    include_default_variant_for_single_digits=True,
)
ctx.lists["user.minutes"] = get_spoken_form_under_one_hundred(
    1,
    59,
    include_oh_variant_for_single_digits=True,
    include_default_variant_for_single_digits=False,
)


@mod.capture(rule="{user.prose_modifiers}")
def prose_modifier(m) -> Callable:
    return getattr(DictationFormat, m.prose_modifiers)


@mod.capture(
    rule="<user.number_string> [(dot | point) <digit_string>] percent [sign|sine]"
)
def prose_percent(m) -> str:
    s = m.number_string
    if hasattr(m, "digit_string"):
        s += "." + m.digit_string
    return s + "%"


@mod.capture(
    rule="<user.number_string> {user.currency} [[and] <user.number_string> [cents|pence]]"
)
def prose_currency(m) -> str:
    s = m.currency + m.number_string_1
    if hasattr(m, "number_string_2"):
        s += "." + m.number_string_2
    return s


@mod.capture(rule="am|pm")
def time_am_pm(m) -> str:
    return str(m)


# this matches eg "twelve thirty-four" -> 12:34 and "twelve hundred" -> 12:00. hmmmmm.
@mod.capture(
    rule="{user.hours} ({user.minutes} | o'clock | hundred hours) [<user.time_am_pm>]"
)
def prose_time_hours_minutes(m) -> str:
    t = m.hours + ":"
    if hasattr(m, "minutes"):
        t += m.minutes
    else:
        t += "00"
    if hasattr(m, "time_am_pm"):
        t += m.time_am_pm
    return t


@mod.capture(rule="{user.hours_twelve} <user.time_am_pm>")
def prose_time_hours_am_pm(m) -> str:
    return m.hours_twelve + m.time_am_pm


@mod.capture(rule="<user.prose_time_hours_minutes> | <user.prose_time_hours_am_pm>")
def prose_time(m) -> str:
    return str(m)


@mod.capture(rule="({user.vocabulary} | <user.abbreviation> | <word>)")
def word(m) -> str:
    """A single word, including user-defined vocabulary."""
    if hasattr(m, "vocabulary"):
        return m.vocabulary
    elif hasattr(m, "abbreviation"):
        return m.abbreviation
    else:
        return " ".join(
            actions.dictate.replace_words(actions.dictate.parse_words(m.word))
        )


@mod.capture(rule="({user.vocabulary} | <phrase>)+")
def text(m) -> str:
    """A sequence of words, including user-defined vocabulary."""
    return format_phrase(m)


@mod.capture(
    rule="({user.vocabulary} | {user.punctuation} | {user.prose_snippets} | <user.prose_currency> | <user.prose_time> | <user.number_prose_prefixed> | <user.prose_percent> | <user.prose_modifier> | <user.abbreviation> | <phrase>)+"
)
def prose(m) -> str:
    """Mixed words and punctuation, auto-spaced & capitalized."""
    # Straighten curly quotes that were introduced to obtain proper spacing.
    return apply_formatting(m).replace("“", '"').replace("”", '"')


@mod.capture(
    rule="({user.vocabulary} | {user.punctuation} | {user.prose_snippets} | <user.prose_currency> | <user.prose_time> | <user.number_prose_prefixed> | <user.prose_percent> | <user.abbreviation> | <phrase>)+"
)
def raw_prose(m) -> str:
    """Mixed words and punctuation, auto-spaced & capitalized, without quote straightening and commands (for use in dictation mode)."""
    return apply_formatting(m)


# For dragon, omit support for abbreviations
@ctx_dragon.capture("user.text", rule="({user.vocabulary} | <phrase>)+")
def text_dragon(m) -> str:
    """A sequence of words, including user-defined vocabulary."""
    return format_phrase(m)


@ctx_dragon.capture(
    "user.prose",
    rule="(<phrase> | {user.vocabulary} | {user.punctuation} | {user.prose_snippets} | <user.prose_currency> | <user.prose_time> | <user.prose_number> | <user.prose_percent> | <user.prose_modifier>)+",
)
def prose_dragon(m) -> str:
    """Mixed words and punctuation, auto-spaced & capitalized."""
    # Straighten curly quotes that were introduced to obtain proper spacing.
    return apply_formatting(m).replace("“", '"').replace("”", '"')


@ctx_dragon.capture(
    "user.raw_prose",
    rule="(<phrase> | {user.vocabulary} | {user.punctuation} | {user.prose_snippets} | <user.prose_currency> | <user.prose_time> | <user.prose_number> | <user.prose_percent>)+",
)
def raw_prose_dragon(m) -> str:
    """Mixed words and punctuation, auto-spaced & capitalized, without quote straightening and commands (for use in dictation mode)."""
    return apply_formatting(m)


# ---------- FORMATTING ---------- #
def format_phrase(m):
    words = capture_to_words(m)
    result = ""
    for i, word in enumerate(words):
        if i > 0 and needs_space_between(words[i - 1], word):
            result += " "
        result += word
    return result


def capture_to_words(m):
    words = []
    for item in m:
        words.extend(
            actions.dictate.replace_words(actions.dictate.parse_words(item))
            if isinstance(item, grammar.vm.Phrase)
            else [item]
        )
    return words


def apply_formatting(m):
    formatter = DictationFormat()
    formatter.state = None
    result = ""
    for item in m:
        # prose modifiers (cap/no cap/no space) produce formatter callbacks.
        if isinstance(item, Callable):
            item(formatter)
        else:
            words = (
                actions.dictate.replace_words(actions.dictate.parse_words(item))
                if isinstance(item, grammar.vm.Phrase)
                else [item]
            )
            for word in words:
                result += formatter.format(word)
    return result


# There must be a simpler way to do this, but I don't see it right now.
no_space_after = re.compile(
    r"""
  (?:
    [\s\-_/#@([{‘“]     # characters that never need space after them
  | (?<!\w)[$£€¥₩₽₹]    # currency symbols not preceded by a word character
  # quotes preceded by beginning of string, space, opening braces, dash, or other quotes
  | (?: ^ | [\s([{\-'"] ) ['"]
  )$""",
    re.VERBOSE,
)
no_space_before = re.compile(
    r"""
  ^(?:
    [\s\-_.,!?/%)\]}’”]   # characters that never need space before them
  | [$£€¥₩₽₹](?!\w)        # currency symbols not followed by a word character
  | [;:](?!-\)|-\()        # colon or semicolon except for smiley faces
  # quotes followed by end of string, space, closing braces, dash, other quotes, or some punctuation.
  | ['"] (?: $ | [\s)\]}\-'".,!?;:/] )
  # apostrophe s
  | 's(?!\w)
  )""",
    re.VERBOSE,
)


def omit_space_before(text: str) -> bool:
    return not text or no_space_before.search(text)


def omit_space_after(text: str) -> bool:
    return not text or no_space_after.search(text)


def needs_space_between(before: str, after: str) -> bool:
    return not (omit_space_after(before) or omit_space_before(after))


# # TESTS, uncomment to enable
# assert needs_space_between("a", "break")
# assert needs_space_between("break", "a")
# assert needs_space_between(".", "a")
# assert needs_space_between("said", "'hello")
# assert needs_space_between("hello'", "said")
# assert needs_space_between("hello.", "'John")
# assert needs_space_between("John.'", "They")
# assert needs_space_between("paid", "$50")
# assert needs_space_between("50$", "payment")
# assert not needs_space_between("", "")
# assert not needs_space_between("a", "")
# assert not needs_space_between("a", " ")
# assert not needs_space_between("", "a")
# assert not needs_space_between(" ", "a")
# assert not needs_space_between("a", ",")
# assert not needs_space_between("'", "a")
# assert not needs_space_between("a", "'")
# assert not needs_space_between("and-", "or")
# assert not needs_space_between("mary", "-kate")
# assert not needs_space_between("$", "50")
# assert not needs_space_between("US", "$")
# assert not needs_space_between("(", ")")
# assert not needs_space_between("(", "e.g.")
# assert not needs_space_between("example", ")")
# assert not needs_space_between("example", '".')
# assert not needs_space_between("example", '."')
# assert not needs_space_between("hello'", ".")
# assert not needs_space_between("hello.", "'")

no_cap_after = re.compile(
    r"""(
    e\.g\.
    | i\.e\.
    )$""",
    re.VERBOSE,
)


def auto_capitalize(text, state=None):
    """
    Auto-capitalizes text. Text must contain complete words, abbreviations, and
    formatted expressions. `state` argument means:

    - None: Don't capitalize initial word.
    - "sentence start": Capitalize initial word.
    - "after newline": Don't capitalize initial word, but we're after a newline.
      Used for double-newline detection.

    Returns (capitalized text, updated state).
    """
    output = ""
    # Imagine a metaphorical "capitalization charge" travelling through the
    # string left-to-right.
    charge = state == "sentence start"
    newline = state == "after newline"
    sentence_end = False
    for c in text:
        # Sentence endings followed by space & double newlines create a charge.
        if (sentence_end and c in " \n\t") or (newline and c == "\n"):
            charge = True
        # Alphanumeric characters and commas/colons absorb charge & try to
        # capitalize (for numbers & punctuation this does nothing, which is what
        # we want).
        elif charge and (c.isalnum() or c in ",:"):
            charge = False
            c = c.capitalize()
        # Otherwise the charge just passes through.
        output += c
        newline = c == "\n"
        sentence_end = c in ".!?" and not no_cap_after.search(output)
    return output, (
        "sentence start"
        if charge or sentence_end
        else "after newline" if newline else None
    )


# ---------- DICTATION AUTO FORMATTING ---------- #
class DictationFormat:
    def __init__(self):
        self.reset()

    def reset(self):
        self.reset_context()
        self.force_no_space = False
        self.force_capitalization = None  # Can also be "cap" or "no cap".

    def reset_context(self):
        self.before = ""
        self.state = "sentence start"

    def update_context(self, before):
        if before is None:
            return
        self.reset_context()
        self.pass_through(before)

    def pass_through(self, text):
        _, self.state = auto_capitalize(text, self.state)
        self.before = text or self.before

    def format(self, text, auto_cap=True):
        if not self.force_no_space and needs_space_between(self.before, text):
            text = " " + text
        self.force_no_space = False
        if auto_cap:
            text, self.state = auto_capitalize(text, self.state)
        if self.force_capitalization == "cap":
            text = format_first_letter(text, lambda s: s.capitalize())
            self.force_capitalization = None
        if self.force_capitalization == "no cap":
            text = format_first_letter(text, lambda s: s.lower())
            self.force_capitalization = None
        self.before = text or self.before
        return text

    # These are used as callbacks by prose modifiers / dictation_mode commands.
    def cap(self):
        self.force_capitalization = "cap"

    def no_cap(self):
        self.force_capitalization = "no cap"

    def no_space(self):
        # This is typically used after repositioning the cursor, so it is helpful to
        # reset capitalization as well.
        #
        # FIXME: this sets state to "sentence start", capitalizing the next
        # word. probably undesirable, since most places are not the start of
        # sentences?
        self.reset_context()
        self.force_no_space = True


def format_first_letter(text, formatter):
    i = -1
    for i, c in enumerate(text):
        if c.isalpha():
            break
    if i >= 0 and i < len(text):
        text = text[:i] + formatter(text[i]) + text[i + 1 :]
    return text


dictation_formatter = DictationFormat()
ui.register("app_deactivate", lambda app: dictation_formatter.reset())
ui.register("win_focus", lambda win: dictation_formatter.reset())


def reformat_last_utterance(formatter):
    text = actions.user.get_last_phrase()
    actions.user.clear_last_phrase()
    text = formatter(text)
    actions.user.add_phrase_to_history(text)
    actions.insert(text)


@mod.action_class
class Actions:
    def dictation_format_reset():
        """Resets the dictation formatter"""
        return dictation_formatter.reset()

    def dictation_format_cap():
        """Sets the dictation formatter to capitalize"""
        dictation_formatter.cap()

    def dictation_format_no_cap():
        """Sets the dictation formatter to not capitalize"""
        dictation_formatter.no_cap()

    def dictation_format_no_space():
        """Sets the dictation formatter to not prepend a space"""
        dictation_formatter.no_space()

    def dictation_reformat_cap():
        """Capitalizes the last utterance"""
        reformat_last_utterance(
            lambda s: format_first_letter(s, lambda c: c.capitalize())
        )

    def dictation_reformat_no_cap():
        """Lowercases the last utterance"""
        reformat_last_utterance(lambda s: format_first_letter(s, lambda c: c.lower()))

    def dictation_reformat_no_space():
        """Removes space before the last utterance"""
        reformat_last_utterance(lambda s: s[1:] if s.startswith(" ") else s)

    def dictation_insert_raw(text: str):
        """Inserts text as-is, without invoking the dictation formatter."""
        actions.user.dictation_insert(text, auto_cap=False)

    def dictation_insert(text: str, auto_cap: bool = True) -> str:
        """Inserts dictated text, formatted appropriately."""
        add_space_after = False
        if settings.get("user.context_sensitive_dictation"):
            # Peek left if we might need leading space or auto-capitalization;
            # peek right if we might need trailing space. NB. We peek right
            # BEFORE insertion to avoid breaking the undo-chain between the
            # inserted text and the trailing space.
            need_left = not omit_space_before(text) or (
                auto_cap and text != auto_capitalize(text, "sentence start")[0]
            )
            need_right = not omit_space_after(text)
            before, after = actions.user.dictation_peek(need_left, need_right)
            dictation_formatter.update_context(before)
            add_space_after = after is not None and needs_space_between(text, after)
        text = dictation_formatter.format(text, auto_cap)
        # Straighten curly quotes that were introduced to obtain proper
        # spacing. The formatter context still has the original curly quotes
        # so that future dictation is properly formatted.
        text = text.replace("“", '"').replace("”", '"')
        actions.user.add_phrase_to_history(text)
        actions.user.insert_between(text, " " if add_space_after else "")

    def dictation_peek(left: bool, right: bool) -> tuple[Optional[str], Optional[str]]:
        """
        Gets text around the cursor to inform auto-spacing and -capitalization.
        Returns (before, after), where `before` is some text before the cursor,
        and `after` some text after it. Results are not guaranteed; `before`
        and/or `after` may be None, indicating no information. If `before` is
        the empty string, this means there is nothing before the cursor (we are
        at the beginning of the document); likewise for `after`.

        To optimize performance, pass `left = False` if you won't need
        `before`, and `right = False` if you won't need `after`.

        dictation_peek() is intended for use before inserting text, so it may
        delete any currently selected text.
        """
        if not (left or right):
            return None, None
        before, after = None, None
        # Inserting a space ensures we select something even if we're at
        # document start; some editors 'helpfully' copy the current line if we
        # edit.copy() while nothing is selected.
        actions.insert(" ")
        if left:
            # In principle the previous word should suffice, but some applications
            # have a funny concept of what the previous word is (for example, they
            # may only take the "`" at the end of "`foo`"). To be double sure we
            # take two words left. I also tried taking a line up + a word left, but
            # edit.extend_up() = key(shift-up) doesn't work consistently in the
            # Slack webapp (sometimes escapes the text box).
            actions.edit.extend_word_left()
            actions.edit.extend_word_left()
            before = actions.edit.selected_text()[:-1]
            # Unfortunately, in web Slack, if our selection ends at newline,
            # this will go right over the newline. Argh.
            actions.edit.right()
        if not right:
            actions.key("backspace")  # remove the space
        else:
            actions.edit.left()  # go left before space
            # We want to select at least two characters to the right, plus the space
            # we inserted, because no_space_before needs two characters in the worst
            # case -- for example, inserting before "' hello" we don't want to add
            # space, while inserted before "'hello" we do.
            #
            # We use 2x extend_word_right() because it's fewer keypresses (lower
            # latency) than 3x extend_right(). Other options all seem to have
            # problems. For instance, extend_line_end() might not select all the way
            # to the next newline if text has been wrapped across multiple lines;
            # extend_line_down() sometimes escapes the current text box (eg. in a
            # browser address bar). 1x extend_word_right() _usually_ works, but on
            # Windows in Firefox it doesn't always select enough characters.
            actions.edit.extend_word_right()
            actions.edit.extend_word_right()
            after = actions.edit.selected_text()[1:]
            actions.edit.left()
            actions.key("delete")  # remove space
        return before, after
