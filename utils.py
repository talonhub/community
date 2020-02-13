from talon.voice import Str, press
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
    Str(s)(None)


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


# FIX ME
def surround(by):
    def func(i, word, last):
        if i == 0:
            word = by + word
        if last:
            word += by
        return word

    return func


# support for parsing numbers as command postfix
def numeral_map():
    numeral_map = dict((str(n), n) for n in range(0, 20))
    for n in [20, 30, 40, 50, 60, 70, 80, 90]:
        numeral_map[str(n)] = n
    numeral_map["oh"] = 0  # synonym for zero
    numeral_map["for"] = 4
    numeral_map["when"] = 1
    return numeral_map


def numerals():
    return " (" + " | ".join(sorted(numeral_map().keys())) + ")+"


def optional_numerals():
    return " (" + " | ".join(sorted(numeral_map().keys())) + ")*"


def text_to_number(m,start_index=0):
    words = [str(s).lower() for s in m[start_index:]]
    result = 0
    for word in words:
        print("word = " + word)
        try:
            result = result + int(word)
        except ValueError:
            result = result

    return result


number_conversions = {"oh": "0", "for": "4", "when": "1", "want": "1"}  # 'oh' => zero
for i, w in enumerate(
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
):
    number_conversions[str(i)] = str(i)
    number_conversions[w] = str(i)
    number_conversions["%s\\number" % (w)] = str(i)

def parse_words_as_integer(m):
    number_list = []
    
    #quick and dirty due to being a python newbie.
    #join the string together, and strip out unneeded garbage
    s = " ".join(m).replace("\\number", "").replace("over", "").lstrip().rstrip();
    
    splits = s.split(" ")
    for split in splits:
        string_to_add = split.lstrip().rstrip()
        if string_to_add in number_conversions:
            number_list.append(number_conversions[string_to_add])
    #reverse the list
    number_list.reverse()
    
    #calculate the value
    result = 0
    place = 1
    for number in number_list:
        result = result + int(number) * place
        place = place * 10
        
    return result

def preserve_clipboard(fn):
    def wrapped_function(*args, **kwargs):
        old = clip.get()
        ret = fn(*args, **kwargs)
        time.sleep(0.1)
        clip.set(old)
        return ret

    return wrapped_function


@preserve_clipboard
def jump_to_target(target):
    press("cmd-left", wait=2000)
    press("cmd-shift-right", wait=2000)
    press("cmd-c", wait=2000)
    press("left", wait=2000)
    line = clip.get()
    print("LINE")
    print(line)
    result = line.find(target)
    if result == -1:
        return
    for i in range(0, result):
        press("right", wait=0)
    for i in range(0, len(target)):
        press("shift-right")
    press("right", wait=0)

def use_mic(mic_name):
    mic = microphone.manager.active_mic()
    if mic is not None and mic.name == mic_name:
        return
    
    mics = {i.name: i for i in list(microphone.manager.menu.items)}
    if mic_name in mics:
        microphone.manager.menu_click(mics[mic_name])