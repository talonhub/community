import logging
import re
from typing import Sequence, Union

from talon import Context, Module, actions
from talon.grammar import Phrase

from .user_settings import append_to_csv, get_list_from_csv

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="additional vocabulary words")


# Default words that will need to be capitalized.
# DON'T EDIT THIS. Edit settings/words_to_replace.csv instead.
# These defaults and those later in this file are ONLY used when
# auto-creating the corresponding settings/*.csv files. Those csv files
# determine the contents of user.vocabulary and dictate.word_map. Once they
# exist, the contents of the lists/dictionaries below are irrelevant.
_capitalize_defaults = [
    # NB. the lexicon now capitalizes January/February by default, but not the
    # others below. Not sure why.
    "January",
    "February",
    # March omitted because it's a regular word too
    "April",
    # May omitted because it's a regular word too
    "June",
    "July",
    "August",  # technically also an adjective but the month is far more common
    "September",
    "October",
    "November",
    "December",
]

# Default words that need to be remapped.
_word_map_defaults = {
    # E.g:
    # "cash": "cache",
    # This is the opposite ordering to words_to_replace.csv (the latter has the target word first)
}
_word_map_defaults.update({word.lower(): word for word in _capitalize_defaults})


# phrases_to_replace is a spoken form -> written form map, used by our
# implementation of `dictate.replace_words` (at bottom of file) to rewrite words
# and phrases Talon recognized. This does not change the priority with which
# Talon recognizes particular phrases over others.
phrases_to_replace = get_list_from_csv(
    "words_to_replace.csv",
    headers=("Replacement", "Original"),
    default=_word_map_defaults,
)

# "dictate.word_map" is used by Talon's built-in default implementation of
# `dictate.replace_words`, but supports only single-word replacements.
# Multi-word phrases are ignored.
ctx.settings["dictate.word_map"] = phrases_to_replace


# Default words that should be added to Talon's vocabulary.
# Don't edit this. Edit 'additional_vocabulary.csv' instead
_simple_vocab_default = ["nmap", "admin", "Cisco", "Citrix", "VPN", "DNS", "Minecraft"]

# Defaults for different pronounciations of words that need to be added to
# Talon's vocabulary.
_default_vocabulary = {
    "N map": "nmap",
    "under documented": "under-documented",
}
_default_vocabulary.update({word: word for word in _simple_vocab_default})

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
vocabulary = get_list_from_csv(
    "additional_words.csv",
    headers=("Word(s)", "Spoken Form (If Different)"),
    default=_default_vocabulary,
)
ctx.lists["user.vocabulary"] = vocabulary


class PhraseReplacer:
    """Utility for replacing phrases by other phrases inside text or word lists.

    Replacing longer phrases has priority.

    Args:
      - phrase_dict: dictionary mapping recognized/spoken forms to written forms
    """

    def __init__(self, phrase_dict: dict[str, str]):
        # Index phrases by first word, then number of subsequent words n_next
        phrase_index = dict()
        for spoken_form, written_form in phrase_dict.items():
            words = spoken_form.split()
            if not words:
                logging.warning(
                    "Found empty spoken form for written form"
                    f"{written_form}, ignored"
                )
                continue
            first_word, n_next = words[0], len(words) - 1
            phrase_index.setdefault(first_word, {}).setdefault(n_next, {})[
                tuple(words[1:])
            ] = written_form

        # Sort n_next index so longer phrases have priority
        self.phrase_index = {
            first_word: sorted(same_first_word.items(), key=lambda x: -x[0])
            for first_word, same_first_word in phrase_index.items()
        }

    def replace(self, input_words: Sequence[str]) -> Sequence[str]:
        input_words = tuple(input_words)  # tuple to ensure hashability of slices
        output_words = []
        first_word_i = 0
        while first_word_i < len(input_words):
            first_word = input_words[first_word_i]
            next_word_i = first_word_i + 1
            # Could this word be the first of a phrase we should replace?
            for n_next, phrases_n_next in self.phrase_index.get(first_word, []):
                # Yes. Perhaps a phrase with n_next subsequent words?
                continuation = input_words[next_word_i : next_word_i + n_next]
                if continuation in phrases_n_next:
                    # Found a match!
                    output_words.append(phrases_n_next[continuation])
                    first_word_i += 1 + n_next
                    break
            else:
                # No match, just add the word to the result
                output_words.append(first_word)
                first_word_i += 1
        return output_words

    # Wrapper used for testing.
    def replace_string(self, text: str) -> str:
        return " ".join(self.replace(text.split()))


# Unit tests for PhraseReplacer
rep = PhraseReplacer(
    {
        "this": "foo",
        "that": "bar",
        "this is": "stopping early",
        "this is a test": "it worked!",
    }
)
assert rep.replace_string("gnork") == "gnork"
assert rep.replace_string("this") == "foo"
assert rep.replace_string("this that this") == "foo bar foo"
assert rep.replace_string("this is a test") == "it worked!"
assert rep.replace_string("well this is a test really") == "well it worked! really"
assert rep.replace_string("try this is too") == "try stopping early too"
assert rep.replace_string("this is a tricky one") == "stopping early a tricky one"

phrase_replacer = PhraseReplacer(phrases_to_replace)


@ctx.action_class("dictate")
class OverwrittenActions:
    def replace_words(words: Sequence[str]) -> Sequence[str]:
        try:
            return phrase_replacer.replace(words)
        except:
            # fall back to default implementation for error-robustness
            logging.error("phrase replacer failed!")
            return actions.next(words)


def _create_vocabulary_entries(spoken_form, written_form, type):
    """Expands the provided spoken form and written form into multiple variants based on
    the provided type, which can be either "name" to add a possessive variant or "noun"
    to add plural.
    """
    entries = {spoken_form: written_form}
    if type == "name":
        # Note that we use the spoken form without apostrophe because this seems to generally lead
        # to better recognition on Conformer b108.
        entries[f"{spoken_form}s"] = f"{written_form}'s"
    elif type == "noun":
        # Note that we simply append an "s", but we could use something more sophisticated like
        # https://github.com/jpvanhal/inflection. The downside is that this is less predictable,
        # and this feature is likely to be used in ways that are unlike common English prose, which
        # is already included in the lexicon. For example, made up identifiers used in programming.
        entries[f"{spoken_form}s"] = f"{written_form}s"
    return entries


# See https://github.com/wolfmanstout/talon-vocabulary-editor for an experimental version
# of this which tests if the default spoken form can be used instead of the provided phrase.
def _add_selection_to_csv(
    phrase: Union[Phrase, str],
    type: str,
    csv: str,
    csv_contents: dict[str, str],
    skip_identical_replacement: bool,
):
    written_form = actions.edit.selected_text().strip()
    if phrase:
        spoken_form = " ".join(actions.dictate.parse_words(phrase))
    else:
        is_acronym = re.fullmatch(r"[A-Z]+", written_form)
        spoken_form = " ".join(written_form) if is_acronym else written_form
    entries = _create_vocabulary_entries(spoken_form, written_form, type)
    new_entries = {}
    added_some_phrases = False
    for spoken_form, written_form in entries.items():
        if skip_identical_replacement and spoken_form == written_form:
            actions.app.notify(f'Skipping identical replacement: "{spoken_form}"')
        elif spoken_form in csv_contents:
            actions.app.notify(f'Spoken form "{spoken_form}" is already in {csv}')
        else:
            new_entries[spoken_form] = written_form
            added_some_phrases = True
    append_to_csv(csv, new_entries)
    if added_some_phrases:
        actions.app.notify(f"Added to {csv}: {new_entries}")


@mod.action_class
class Actions:
    def add_selection_to_vocabulary(phrase: Union[Phrase, str] = "", type: str = ""):
        """Permanently adds the currently selected text to the vocabulary with the provided
        spoken form and adds variants based on the type ("noun" or "name").
        """
        _add_selection_to_csv(
            phrase,
            type,
            "additional_words.csv",
            vocabulary,
            False,
        )

    def add_selection_to_words_to_replace(phrase: Phrase, type: str = ""):
        """Permanently adds the currently selected text as replacement for the provided
        original form and adds variants based on the type ("noun" or "name").
        """
        _add_selection_to_csv(
            phrase,
            type,
            "words_to_replace.csv",
            phrases_to_replace,
            True,
        )
