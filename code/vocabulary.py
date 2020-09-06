from talon import Context, Module, actions, grammar

# Add single words here if Talon recognizes them, but they need to have their
# capitalization adjusted.
capitalize = [
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

# Add single words here if Talon recognizes them, but they need to have their
# spelling adjusted.
word_map = {
    # For example:
    # "color": "colour",
}
word_map.update({x.lower(): x for x in capitalize})

# Add words (or phrases you want treated as words) here if Talon doesn't
# recognize them at all.
simple_vocabulary = ["nmap", "admin", "Cisco", "Citrix", "VPN", "DNS", "minecraft"]

# Add vocabulary words (or phrases you want treated as words) here that aren't
# recognized by Talon and are written differently than they're pronounced.
mapping_vocabulary = {
    # For example:
    # "enn map": "nmap",
    # "under documented": "under-documented",
}
mapping_vocabulary.update(dict(zip(simple_vocabulary, simple_vocabulary)))


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

# dictate.word_map is used by actions.dictate.replace_words to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
ctx.settings["dictate.word_map"] = word_map

# user.vocabulary is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
ctx.lists["user.vocabulary"] = mapping_vocabulary
