from talon import app, Module, Context, actions
from talon.voice import press, Capture, Str

from talon.engine import engine
import string

alpha_alt = "air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip".split()
f_keys = {f"F {i}": f"f{i}" for i in range(1, 13)}
# arrows are separated because 'up' has a high false positive rate
arrows = ["left", "right", "up", "down"]
simple_keys = ["tab", "escape", "enter", "space", "pageup", "pagedown", "home", "end"]
alternate_keys = {"delete": "backspace", "forward delete": "delete"}

modifiers_dict = {
    "control": "ctrl",
    "shift": "shift",
    "alt": "alt",
}

if app.platform == "mac":
    modifiers_dict["command"] = "cmd"
    modifiers_dict["option"] = "alt"
elif app.platform == "windows":
    modifiers_dict["windows"] = "win"
    modifiers_dict["super"] = "win"
elif app.platform == "linux":
    modifiers_dict["super"] = "super"

alphabet_dict = dict(zip(alpha_alt, string.ascii_lowercase))
digits = {
    "zero":  "0",
    "one":   "1",
    "two":   "2",
    "three": "3",
    "four":  "4",
    "five":  "5",
    "six":   "6",
    "seven": "7",
    "eight": "8",
    "nine":  "9",
}

symbols = {
    "back tick": "`",
    "comma": ",",
    "dot": ".",
    "period": ".",
    "semi": ";",
    "semicolon": ";",
    "quote": "'",
    "L square": "[",
    "left square": "[",
    "square": "[",
    "R square": "]",
    "right square": "]",
    "forward slash": "/",
    "slash": "/",
    "backslash": "\\",
    "minus": "-",
    "dash": "-",
    "equals": "=",
}

simple_keys = {k: k for k in simple_keys}
arrows_dict = {k: k for k in arrows}
keys = {}
keys.update(f_keys)
keys.update(simple_keys)
keys.update(alternate_keys)
keys.update(symbols)

# # map alnum and keys separately so engine gives priority to letter/number repeats
keymap = keys.copy()
keymap.update(arrows_dict)
keymap.update(alphabet_dict)
keymap.update(digits)

def insert(s):
    Str(s)(None)

def get_modifiers(m):
    if m is None:
        return None
        
    try:
        return [modifiers_dict[word] for word in m._words]
    except KeyError:
        return []

def get_alaphabet(m):
    try:
        return [alphabet_dict[word] for word in m._words]
    except KeyError:
        return []
        
def get_arrows(m):
    try:
        print(str(m))
        return [arrows_dict[word] for word in m._words]
    except KeyError:
        return []

def get_digits(m):
    try:
        return [digits[mod] for mod in digits]
    except KeyError:
        return []

def get_keys(m):
    try:
        return [keymap[k] for k in m._words]
    except KeyError:
        pass
    return []

def uppercase_letters(m):
    insert("".join(get_keys(m)).upper())

def start(m):
    press("super")

def press_keys(mod_capture, key_capture):
    mods = get_modifiers(mod_capture)
    keys = get_keys(key_capture)
    if mods:
        press("-".join(mods + [keys[0]]))
        keys = keys[1:]
    for k in keys:
        press(k)

def uppercase_letters(m):
    insert("".join(get_keys(m)).upper())
    
def letters(m):
    insert("".join(get_keys(m)).lower())
    
ctx = Context()

modifiers_rule = '(' + ('|'.join(modifiers_dict.keys())) + ')'
@ctx.capture('modifiers', rule=f'{modifiers_rule}')
def modifiers(m):
    return m
    
alphabet_rule = '(' + ('|'.join( alphabet_dict.keys())) + ')'
@ctx.capture('alphabet', rule=f'{alphabet_rule}')
def alphabet(m):
    return m

keys_rule = '(' + ('|'.join( keymap.keys())) + ')'
@ctx.capture('keys', rule=f'{keys_rule}+')
def keys(m):    
    return m

arrows_rule = '(' + ('|'.join( arrows_dict.keys())) + ')'
@ctx.capture('arrows', rule=f'{arrows_rule}+')
def arrows(m):
    return m

mod = Module()
@mod.action_class
class Actions:  
    def keys_with_modifiers(mods: Capture, keys: Capture):
        """keys_with_modifiers"""
        press_keys(mods, keys)
        
    def keys(keys: Capture):
        """keys"""
        press_keys(None, keys)
            
    def uppercase_letters(m: Capture):
        """keys"""
        uppercase_letters(m)
        
    def letters(m: Capture):
        """keys"""
        letters(m)