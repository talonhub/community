from collections import OrderedDict
import logging
from typing import Dict, Union

from talon import Context, Module
from .user_settings import get_list_from_csv

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="additional vocabulary words")


# Default words that will need to be capitalized (particularly under w2l).
# NB. These defaults and those later in this file are ONLY used when
# auto-creating the corresponding settings/*.csv files. Those csv files
# determine the contents of user.vocabulary and dictate.word_map. Once they
# exist, the contents of the lists/dictionaries below are irrelevant.
_capitalize_defaults = [
    "I",
    "I'm",
    "I've",
    "I'll",
    "I'd",
    "Monday",
    "Mondays",
    "Tuesday",
    "Tuesdays",
    "Wednesday",
    "Wednesdays",
    "Thursday",
    "Thursdays",
    "Friday",
    "Fridays",
    "Saturday",
    "Saturdays",
    "Sunday",
    "Sundays",
    "January",
    "February",
    # March omitted because it's a regular word too
    "April",
    # May omitted because it's a regular word too
    "June",
    "July",
    "August",
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


# phrases_to_replace is a spoken form -> written form map, used by
# `user.replace_phrases` to rewrite words and phrases Talon recognized.
# This does not change the priority with which Talon recognizes
# particular phrases over others.
phrases_to_replace = get_list_from_csv(
    "words_to_replace.csv",
    headers=("Replacement", "Original"),
    default=_word_map_defaults
)

# "dictate.word_map" is used by `actions.dictate.replace_words`;
# a built-in Talon action similar to `replace_phrases`, but supporting
# only single-word replacements. Multi-word phrases are ignored.
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
ctx.lists["user.vocabulary"] = get_list_from_csv(
    "additional_words.csv",
    headers=("Word(s)", "Spoken Form (If Different)"),
    default=_default_vocabulary,
)

# for quick verification of the reload
# print(str(ctx.settings["dictate.word_map"]))
# print(str(ctx.lists["user.vocabulary"]))


class PhraseReplacer:
    """Utility for replacing phrases by other phrases inside text or word lists.

    Replacing longer phrases has priority.

    Args:
      - phrase_dict: dictionary mapping recognized/spoken forms to written forms
    """

    def __init__(self, phrase_dict: Dict[str, str]):
        # Index phrases by first word, then number of subsequent words n_next
        phrase_index = dict()
        for spoken_form, written_form in phrase_dict.items():
            words = spoken_form.split()
            if not words:
                logging.warning("Found empty spoken form for written form"
                                f"{written_form}, ignored")
                continue
            first_word, n_next = words[0], len(words) - 1
            phrase_index.setdefault(first_word, dict())
            same_first_word = phrase_index[first_word]
            same_first_word.setdefault(n_next, dict())
            same_first_word[n_next][tuple(words[1:])] = written_form

        # Sort n_next index so longer phrases have priority
        self.phrase_index = {
            first_word: OrderedDict(sorted(same_first_word.items(), key=lambda x: -x[0]))
            for first_word, same_first_word in phrase_index.items()
        }

    def replace_phrases(self, input_text: Union[str, list, tuple]):
        """Return input_text with phrases replaced"""
        got_string = isinstance(input_text, str)
        if got_string:
            input_text = input_text.split()
        input_words = tuple(input_text)

        output_words = []
        first_word_i = 0
        while first_word_i <= len(input_words) - 1:
            first_word = input_words[first_word_i]
            next_word_i = first_word_i + 1
            # Could this word be the first of a phrase we should replace?
            for n_next, phrases_n_next in self.phrase_index.get(first_word, dict()).items():
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

        if got_string:
            return ' '.join(output_words)
        return output_words


# Unit tests for PhraseReplacer
rep = PhraseReplacer({
    'this': 'foo',
    'that': 'bar',
    'this is': 'stopping early',
    'this is a test': 'it worked!',
})
assert rep.replace_phrases('gnork') == 'gnork'
assert rep.replace_phrases('this') == 'foo'
assert rep.replace_phrases('this that this') == 'foo bar foo'
assert rep.replace_phrases('this is a test') == 'it worked!'
assert rep.replace_phrases('well this is a test really') == 'well it worked! really'
assert rep.replace_phrases('try this is too') == 'try stopping early too'
assert rep.replace_phrases('this is a tricky one') == 'stopping early a tricky one'


phrase_replacer = PhraseReplacer(phrases_to_replace)

@mod.action_class
class Actions:

    def replace_phrases(input_text: str):
        """Replace phrases in input_text"""
        return phrase_replacer.replace_phrases(input_text)
