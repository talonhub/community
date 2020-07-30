from talon import Context, Module, actions, grammar


simple_vocabulary = [
    "nmap",
    "admin",
    "Cisco",
    "Citrix",
    "VPN",
    "DNS",
    "minecraft",
]

mapping_vocabulary = {
    "i": "I",
    "i'm": "I'm",
    "i've": "I've",
    "i'll": "I'll",
    "i'd": "I'd",
}

mapping_vocabulary.update(dict(zip(simple_vocabulary, simple_vocabulary)))

mod = Module()


def remove_dragon_junk(word):
    return str(word).lstrip("\\").split("\\")[0]


@mod.capture(rule="({user.vocabulary})")
def vocabulary(m) -> str:
    return m.vocabulary


@mod.capture(rule="(<user.vocabulary> | <word>)")
def word(m) -> str:
    try:
        return m.vocabulary
    except AttributeError:
        return remove_dragon_junk(m.word)


punctuation = set(".,-!?;:")


@mod.capture(rule="(<user.vocabulary> | <phrase>)+")
def text(m) -> str:
    words = []
    result = ""
    for item in m:
        if isinstance(item, grammar.vm.Phrase):
            words = words + actions.dictate.parse_words(item)
        else:
            words = words + item.split(" ")

    for i, word in enumerate(words):
        if i > 0 and word not in punctuation:
            result += " "

        result += word

    return result


mod.list("vocabulary", desc="user vocabulary")

ctx = Context()

# setup the word map too
ctx.settings["dictate.word_map"] = mapping_vocabulary
ctx.lists["user.vocabulary"] = mapping_vocabulary
