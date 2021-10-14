# Descended from https://github.com/dwiel/talon_community/blob/master/misc/dictation.py
from talon import Module, Context, ui, actions, clip, app, grammar
from typing import Optional, Tuple, Literal
import re

mod = Module()

setting_context_sensitive_dictation = mod.setting(
    "context_sensitive_dictation",
    type=bool,
    default=False,
    desc="Look at surrounding text to improve auto-capitalization/spacing in dictation mode. By default, this works by selecting that text & copying it to the clipboard, so it may be slow or fail in some applications.",
)

@mod.capture(rule="({user.vocabulary} | <word>)")
def word(m) -> str:
    """A single word, including user-defined vocabulary."""
    try:
        return m.vocabulary
    except AttributeError:
        return " ".join(actions.dictate.replace_words(actions.dictate.parse_words(m.word)))

@mod.capture(rule="({user.vocabulary} | <phrase>)+")
def text(m) -> str:
    """A sequence of words, including user-defined vocabulary."""
    return format_phrase(m)

@mod.capture(rule="({user.vocabulary} | {user.punctuation} | <phrase>)+")
def prose(m) -> str:
    """Mixed words and punctuation, auto-spaced & capitalized."""
    text, _state = auto_capitalize(format_phrase(m))
    return text


# ---------- FORMATTING ---------- #
def format_phrase(m):
    words = capture_to_words(m)
    result = ""
    for i, word in enumerate(words):
        if i > 0 and needs_space_between(words[i-1], word):
            result += " "
        result += word
    return result

def capture_to_words(m):
    words = []
    for item in m:
        words.extend(
            actions.dictate.replace_words(actions.dictate.parse_words(item))
            if isinstance(item, grammar.vm.Phrase) else
            item.split(" "))
    return words

# There must be a simpler way to do this, but I don't see it right now.
no_space_after = re.compile(r"""
  (?:
    [\s\-_/#@([{‘“]     # characters that never need space after them
  | (?<!\w)[$£€¥₩₽₹]    # currency symbols not preceded by a word character
  # quotes preceded by beginning of string, space, opening braces, dash, or other quotes
  | (?: ^ | [\s([{\-'"] ) ['"]
  )$""", re.VERBOSE)
no_space_before = re.compile(r"""
  ^(?:
    [\s\-_.,!?;:/%)\]}’”]   # characters that never need space before them
  | [$£€¥₩₽₹](?!\w)         # currency symbols not followed by a word character
  # quotes followed by end of string, space, closing braces, dash, other quotes, or some punctuation.
  | ['"] (?: $ | [\s)\]}\-'".,!?;:/] )
  )""", re.VERBOSE)

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

def auto_capitalize(text, state = None):
    """
    Auto-capitalizes text. `state` argument means:

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
    for c in text:
        # Sentence endings & double newlines create a charge.
        if c in ".!?" or (newline and c == "\n"):
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
    return output, ("sentence start" if charge else
                    "after newline" if newline else None)


# ---------- DICTATION AUTO FORMATTING ---------- #
class DictationFormat:
    def __init__(self):
        self.reset()

    def reset(self):
        self.before = ""
        self.state = "sentence start"

    def update_context(self, before):
        if before is None: return
        self.reset()
        self.pass_through(before)

    def pass_through(self, text):
        _, self.state = auto_capitalize(text, self.state)
        self.before = text or self.before

    def format(self, text):
        if needs_space_between(self.before, text):
            text = " " + text
        text, self.state = auto_capitalize(text, self.state)
        self.before = text or self.before
        return text

dictation_formatter = DictationFormat()
ui.register("app_deactivate", lambda app: dictation_formatter.reset())
ui.register("win_focus", lambda win: dictation_formatter.reset())

@mod.action_class
class Actions:
    def dictation_format_reset():
        """Resets the dictation formatter"""
        return dictation_formatter.reset()

    def dictation_insert_raw(text: str):
        """Inserts text as-is, without invoking the dictation formatter."""
        dictation_formatter.pass_through(text)
        actions.insert(text)

    def dictation_insert(text: str) -> str:
        """Inserts dictated text, formatted appropriately."""
        context_sensitive = setting_context_sensitive_dictation.get()
        # Omit peeking left if we don't need left space or capitalization.
        if (context_sensitive
            and not (omit_space_before(text)
                     and auto_capitalize(text, "sentence start")[0] == text)):
            dictation_formatter.update_context(
                actions.user.dictation_peek_left(clobber=True))
        text = dictation_formatter.format(text)
        actions.user.add_phrase_to_history(text)
        actions.insert(text)
        # Add a space after cursor if necessary.
        if not context_sensitive or omit_space_after(text):
            return
        char = actions.user.dictation_peek_right()
        if char is not None and needs_space_between(text, char):
            actions.insert(" ")
            actions.edit.left()

    def dictation_peek_left(clobber: bool = False) -> Optional[str]:
        """
        Tries to get some text before the cursor, ideally a word or two, for the
        purpose of auto-spacing & -capitalization. Results are not guaranteed;
        dictation_peek_left() may return None to indicate no information. (Note
        that returning the empty string "" indicates there is nothing before
        cursor, ie. we are at the beginning of the document.)

        If there is currently a selection, dictation_peek_left() must leave it
        unchanged unless `clobber` is true, in which case it may clobber it.
        """
        # Get rid of the selection if it exists.
        if clobber: actions.user.clobber_selection_if_exists()
        # Otherwise, if there's a selection, fail.
        elif "" != actions.edit.selected_text(): return None

        # In principle the previous word should suffice, but some applications
        # have a funny concept of what the previous word is (for example, they
        # may only take the "`" at the end of "`foo`"). To be double sure we
        # take two words left. I also tried taking a line up + a word left, but
        # edit.extend_up() = key(shift-up) doesn't work consistently in the
        # Slack webapp (sometimes escapes the text box).
        actions.edit.extend_word_left()
        actions.edit.extend_word_left()
        text = actions.edit.selected_text()
        # if we're at the beginning of the document/text box, we may not have
        # selected any text, in which case we shouldn't move the cursor.
        if text:
            # Unfortunately, in web Slack, if our selection ends at newline,
            # this will go right over the newline. Argh.
            actions.edit.right()
        return text

    def clobber_selection_if_exists():
        """Deletes the currently selected text if it exists; otherwise does nothing."""
        actions.key("space backspace")
        # This space-backspace trick is fast and reliable but has the
        # side-effect of cluttering the undo history. Other options:
        #
        # 1. Call edit.cut() inside a clip.revert() block. This assumes
        #    edit.cut() is supported AND will be a no-op if there's no
        #    selection. Unfortunately, sometimes one or both of these is false,
        #    eg. the notion webapp makes ctrl-x cut the current block by default
        #    if nothing is selected.
        #
        # 2. Test whether a selection exists by asking whether
        #    edit.selected_text() is empty; if it does, use edit.delete(). This
        #    usually uses the clipboard, which can be quite slow. Also, not sure
        #    how this would interact with switching edit.selected_text() to use
        #    the selection clipboard on linux, which can be nonempty even if no
        #    text is selected in the current application.
        #
        # Perhaps this ought to be configurable by a setting.

    def dictation_peek_right() -> Optional[str]:
        """
        Tries to get a few characters after the cursor for auto-spacing.
        Results are not guaranteed; dictation_peek_right() may return None to
        indicate no information. (Note that returning the empty string ""
        indicates there is nothing after cursor, ie. we are at the end of the
        document.)
        """
        # We grab two characters because I think that's what no_space_before
        # needs in the worst case. An example where the second character matters
        # is inserting before (1) "' hello" vs (2) "'hello". In case (1) we
        # don't want to add space, in case (2) we do.
        actions.edit.extend_right()
        actions.edit.extend_right()
        after = actions.edit.selected_text()
        if after: actions.edit.left()
        return after

# Use the dictation formatter in dictation mode.
dictation_ctx = Context()
dictation_ctx.matches = r"""
mode: dictation
"""

@dictation_ctx.action_class("main")
class main_action:
    def auto_insert(text): actions.user.dictation_insert(text)
