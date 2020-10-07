from talon import Module, Context, ui, actions

mod = Module()
ctx = Context()
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
        self.last_utterance = None
        self.paused = False
        ui.register("app_deactivate", lambda app: self.reset())
        ui.register("win_focus", lambda win: self.reset())

    def reset(self):
        self.caps = True
        self.space = False

    def pause(self, paused):
        self.paused = paused

    def format(self, text):
        if self.paused:
            self.last_utterance = text
            return text

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
                result += " "

            if self.caps:
                word = word.capitalize()

            result += word
            self.space = "\n" not in word and word[-1] not in no_space_after_these
            self.caps = is_sentence_end
            self.last_utterance = result

        return result


auto_formatter = AutoFormat()
ctx.matches = r"""
mode: dictation 
"""


@ctx.action_class("main")
class main_action:
    def auto_format(text: str) -> str:
        return auto_formatter.format(text)


@mod.action_class
class Actions:
    def auto_format_pause():
        """Pauses the autoformatter"""
        return auto_formatter.pause(True)

    def auto_format_resume():
        """Resumes the autoformatter"""
        return auto_formatter.pause(False)

    def auto_format_reset():
        """Resumes the autoformatter"""
        return auto_formatter.reset()

    def clear_last_utterance():
        """Resumes the autoformatter"""
        if auto_formatter.last_utterance:
            for c in auto_formatter.last_utterance:
                actions.edit.delete()

    def select_last_utterance():
        """Selects the last utterance"""
        if auto_formatter.last_utterance:
            for c in auto_formatter.last_utterance:
                actions.edit.extend_left()
