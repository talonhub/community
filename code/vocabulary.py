from talon import Context, Module


mod = Module()

class TextObject:
    def __init__(self, m):
        self.words = list(str(m).split(" "))
        self.text = " ".join(self.words)


@mod.capture(rule='({user.vocabulary} | <word>)')
def word(m) -> str:
    try: return m.vocabulary
    except AttributeError: return m.word


@mod.capture(rule="(<user.word> | <phrase>)+")
def text(m) -> str:
    return TextObject(m).text


@mod.capture(rule="({user.vocabulary} | <phrase>)+")
def textObject(m) -> str:
    return TextObject(m)


mod.list("vocabulary", desc="user vocabulary")