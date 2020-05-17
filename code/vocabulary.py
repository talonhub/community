from talon import Context, Module

# Sometimes my capture results in vocabulary words getting inserted as the key
# with the '@' prefix instead of the value, and idk why, but this fixes it by
# manually mapping those in post
def word_map_bug_fix(word: str) -> str:
    if word[0] == "@":
        return mapping_vocabulary[word[1:]] or word
    else:
        return word


mod = Module()


class TextObject:
    def __init__(self, m):
        self.words = list(map(word_map_bug_fix, str(m).split(" ")))
        self.text = " ".join(self.words)


@mod.capture(rule="{user.vocabulary}")
def word(m) -> str:
    return m.vocabulary


@mod.capture(rule="(<user.word> | <phrase>)+")
def text(m) -> str:
    return TextObject(m).text


@mod.capture(rule="(<user.word> | <phrase>)+")
def textObject(m) -> str:
    return TextObject(m)


mod.list("vocabulary", desc="user vocabulary")
