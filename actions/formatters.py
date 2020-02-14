from talon import Module, Context, actions, ui
from talon.voice import Capture, Str
from ..utils import surround, sentence_text, text, parse_word, parse_words

ctx = Context()
key = actions.key

words_to_keep_lowercase = "a,an,the,at,by,for,in,is,of,on,to,up,and,as,but,or,nor".split(",")

def get_formatted_string(words, fmt):
    tmp = []
    spaces = True
    for i, w in enumerate(words):
        w = parse_word(w)
        smash, func = formatters[fmt]
        w = func(i, w, i == len(words) - 1)
        spaces = spaces and not smash
        tmp.append(w)
        
    words = tmp
    sep = " "
    if not spaces:
        sep = ""
    return sep.join(words)

def FormatText(m):
    fmt = []
    if m._words[-1] == "over":
        m._words = m._words[:-1]
    for w in m._words:
        if isinstance(w, Word):
            fmt.append(w.word)
    try:
        words = parse_words(m)
    except AttributeError:
        with clip.capture() as s:
            edit.copy()
        words = s.get().split(" ")
        if not words:
            return

    tmp = []
    spaces = True
    for i, w in enumerate(words):
        w = parse_word(w)
        for name in reversed(fmt):
            smash, func = formatters[name]
            w = func(i, w, i == len(words) - 1)
            spaces = spaces and not smash
        tmp.append(w)
    words = tmp

    sep = " "
    if not spaces:
        sep = ""
    Str(sep.join(words))(None)

formatters = {
    # True -> no separator
    "dunder": (True, lambda i, word, _: "__%s__" % word if i == 0 else word),
    "camel": (True, lambda i, word, _: word if i == 0 else word.capitalize()),
    "hammer" : (True, lambda i, word, _: word.capitalize()),
    "snake": (True, lambda i, word, _: word.lower() if i == 0 else "_" + word.lower()),
    "smash": (True, lambda i, word, _: word),
    "kebab": (True, lambda i, word, _: word if i == 0 else "-" + word),
    "packed": (True, lambda i, word, _: word if i == 0 else "::" + word),
    "allcaps": (False, lambda i, word, _: word.upper()),
    "alldown": (False, lambda i, word, _: word.lower()),
    "dubstring": (False, surround('"')),
    "string": (False, surround("'")),
    "padded": (False, surround(" ")),
    "dotted": (True, lambda i, word, _: word if i == 0 else "." + word),
    "slasher": (True, lambda i, word, _: "/" + word),
    "sentence": (False, lambda i, word, _: word.capitalize() if i == 0 else word),
    "title": (False, lambda i, word, _:  word.capitalize() if i == 0 or word not in words_to_keep_lowercase else word)
}

mod = Module()
mod.list('formatters', desc='list of formatters')

@mod.action_class
class Actions:
    def to_sentence(m: Capture):
        """Sentence formatter"""
        sentence_text(m)
        
    def to_text(m: Capture):
        """text formatter"""
        text(m)

@ctx.capture('format_text', rule='{self.formatters} <dgndictation>')
def format_text(m):
    print("formatter: " + str(m._words))
    return get_formatted_string(m._words[1:], m.formatters[0])

ctx.lists['self.formatters'] = formatters.keys()
