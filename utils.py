from talon import actions
import talon.clip as clip
from talon import resource
import json
import os
import time
from talon_plugins import microphone

# overrides are used as a last resort to override the output. Some uses:
# - frequently misheard words
# - force homophone preference (alternate homophones can be accessed with homophones command)

# To add an override, add the word to override as the key and desired replacement as value in overrides.json
mapping = json.load(resource.open("overrides.json"))

# used for auto-spacing
punctuation = set(".,-!?")

def remove_dragon_junk(word):
    return str(word).lstrip("\\").split("\\")[0]


def parse_word(word):
    word = remove_dragon_junk(word)
    word = mapping.get(word.lower(), word)
    return word

def join_words(words, sep=" "):
    out = ""
    for i, word in enumerate(words):
        if i > 0 and word not in punctuation:
            out += sep
        out += word
    return out


def parse_words(m):
    return list(map(parse_word, m._words))

def insert(s):
    actions.insert(s)

def text(m):
    insert(join_words(parse_words(m)).lower())

def sentence_text(m):
    text = join_words(parse_words(m)).lower()
    insert(text.capitalize())

def word(m):
    text = extract_word(m)
    insert(text.lower())

def extract_word(m):
    return join_words(list(map(parse_word, m.dgnwords.words)))

def preserve_clipboard(fn):
    def wrapped_function(*args, **kwargs):
        old = clip.get()
        ret = fn(*args, **kwargs)
        time.sleep(0.1)
        clip.set(old)
        return ret

    return wrapped_function

def use_mic(mic_name):
    mic = microphone.manager.active_mic()
    if mic is not None and mic.name == mic_name:
        return
    
    mics = {i.name: i for i in list(microphone.manager.menu.items)}
    if mic_name in mics:
        microphone.manager.menu_click(mics[mic_name])