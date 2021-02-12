from talon import Module
from .user_settings import bind_list_to_csv, bind_word_map_to_csv

mod = Module()

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
}
_word_map_defaults.update({word.lower(): word for word in _capitalize_defaults})

# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
bind_word_map_to_csv(
    "words_to_replace.csv",
    csv_headers=("Replacement", "Original"),
    default_values=_word_map_defaults,
)


# Default words that should be added to Talon's vocabulary.
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
bind_list_to_csv(
    "user.vocabulary",
    "additional_words.csv",
    csv_headers=("Word(s)", "Spoken Form (If Different)"),
    default_values=_default_vocabulary,
)
