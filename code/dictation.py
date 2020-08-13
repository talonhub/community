from talon import Module, ui, actions

mod = Module()

# Courtesy of https://github.com/dwiel/talon_community/blob/master/misc/dictation.py
# Port for Talon's new api + wav2letter

# dictionary of sentence ends. No space should appear before these.
sentence_ends = {
    ".": ".",
    "?": "?",
    "!": "!",
    # these are mapped with names since passing "\n" didn't work for reasons
    "new-paragraph": "\n\n",
    "new-line": "\n",
}

# dictionary of punctuation. no space before these.
punctuation = {
    ",": ",",
    ":": ":",
    ";": ";",
    "-": "-",
    "/": "/",
    "-": "-",
    ")": ")",
}

no_space_after_these = set("-/(")


class AutoFormat:
    def __init__(self):
        self.reset()
        ui.register("app_deactivate", lambda app: self.reset())
        ui.register("win_focus", lambda win: self.reset())

    def reset(self):
        self.caps = True
        self.space = False

    def insert(self, text):
        result = ""
        for word in text.split():
            is_sentence_end = False
            is_punctuation = False
            if word in sentence_ends:
                word = sentence_ends[word]
                is_sentence_end = True

            elif word in punctuation:
                word = punctuation[word]
                # do  nothing
                is_punctuation = True

            elif self.space:
                actions.insert(" ")

            if self.caps:
                word = word.capitalize()

            actions.insert(word)
            self.space = "\n" not in word and word[-1] not in no_space_after_these
            self.caps = is_sentence_end


auto_format = AutoFormat()


@mod.action_class
class Actions:
    def dictate(text: str):
        """Insert auto formatted text"""
        auto_format.insert(text)
