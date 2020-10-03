from talon import Context, Module, actions, grammar
from .user_settings import bind_list_to_csv, bind_word_map_to_csv


# Default words that will need to be capitalized (particularly under w2l).
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

# Default words that should be added to Talon's vocabulary.
_simple_vocab_default = ["nmap", "admin", "Cisco", "Citrix", "VPN", "DNS", "Minecraft"]

# Defaults for different pronounciations of words that need to be added to
# Talon's vocabulary.
_mapping_vocab_default = {
    "N map": "nmap",
    "under documented": "under-documented",
}


mod = Module()


@mod.capture(rule="{user.vocabulary}")
def vocabulary(m) -> str:
    return m.vocabulary


@mod.capture(rule="(<user.vocabulary> | <word>)")
def word(m) -> str:
    try:
        return m.vocabulary
    except AttributeError:
        # TODO: if the word is both a regular word AND user.vocabulary, then in
        # principle it may parse as <word> instead; we ought to pass it through
        # mapping_vocabulary to be sure. But we should be doing that in
        # user.text, below, too.
        words = actions.dictate.replace_words(actions.dictate.parse_words(m.word))
        assert len(words) == 1
        return words[0]


punctuation = set(".,-!?;:")


@mod.capture(rule="(<user.vocabulary> | <phrase>)+")
def text(m) -> str:
    words = []
    for item in m:
        if isinstance(item, grammar.vm.Phrase):
            words.extend(
                actions.dictate.replace_words(actions.dictate.parse_words(item))
            )
        else:
            words.extend(item.split(" "))

    result = ""
    for i, word in enumerate(words):
        if i > 0 and word not in punctuation and words[i - 1][-1] not in ("/-("):
            result += " "
        result += word
    return result


mod.list("vocabulary", desc="user vocabulary")

ctx = Context()


_default_word_map = {}
_default_word_map.update(_word_map_defaults)
_default_word_map.update({word.lower(): word for word in _capitalize_defaults})
# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
bind_word_map_to_csv(
    "words_to_replace.csv",
    csv_headers=("Replacement", "Original"),
    default_values=_default_word_map,
)

_default_vocabulary = {}
_default_vocabulary.update({word: word for word in _simple_vocab_default})
_default_vocabulary.update(_mapping_vocab_default)
# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
bind_list_to_csv(
    "user.vocabulary",
    "additional_words.csv",
    csv_headers=("Word(s)", "Spoken Form (If Different)"),
    default_values=_default_vocabulary,
)
