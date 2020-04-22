#intended for dictation mode
from talon import Context
ctx = Context()
#in case we need to match
# ctx.matches = r'''
# mode: dictation
# '''
ctx.settings['dictate.word_map'] = {
    'i': 'I',
    "i'm": "I'm",
    "i've": "I've",
    "i'd": "I'd",
}