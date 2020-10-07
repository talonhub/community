from typing import Set

from talon import Module, Context, actions
import sys

default_alphabet = "air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip".split(
    " "
)
letters_string = "abcdefghijklmnopqrstuvwxyz"

default_digits = "zero one two three four five six seven eight nine".split(" ")
numbers = [str(i) for i in range(10)]
default_f_digits = "one two three four five six seven eight nine ten eleven twelve".split(
    " "
)

mod = Module()
mod.list("letter", desc="The spoken phonetic alphabet")
mod.list("symbol_key", desc="All symbols from the keyboard")
mod.list("arrow_key", desc="All arrow keys")
mod.list("number_key", desc="All number keys")
mod.list("modifier_key", desc="All modifier keys")
mod.list("function_key", desc="All function keys")
mod.list("special_key", desc="All special keys")


@mod.capture
def modifiers(m) -> str:
    "One or more modifier keys"


@mod.capture
def arrow_key(m) -> str:
    "One directional arrow key"


@mod.capture
def arrow_keys(m) -> str:
    "One or more arrow keys separated by a space"


@mod.capture
def number_key(m) -> str:
    "One number key"


@mod.capture
def letter(m) -> str:
    "One letter key"


@mod.capture
def letters(m) -> str:
    "Multiple letter keys"


@mod.capture
def symbol_key(m) -> str:
    "One symbol key"


@mod.capture
def function_key(m) -> str:
    "One function key"


@mod.capture
def special_key(m) -> str:
    "One special key"


@mod.capture
def unmodified_key(m) -> str:
    "A single key with no modifiers"


@mod.capture
def key(m) -> str:
    "A single key with optional modifiers"


@mod.capture
def keys(m) -> str:
    "A sequence of one or more keys with optional modifiers"


ctx = Context()
ctx.lists["self.modifier_key"] = {
    "alt": "alt",
    "command": "cmd",
    "control": "ctrl",  #'troll':   'ctrl',
    "option": "alt",
    "shift": "shift",  #'sky':     'shift',
    "super": "super",
}
alphabet = dict(zip(default_alphabet, letters_string))
ctx.lists["self.letter"] = alphabet
ctx.lists["self.symbol_key"] = {
    "back tick": "`",
    "`": "`",
    "comma": ",",
    ",": ",",
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
    "plus": "+",
    "question mark": "?",
    "tilde": "~",
    "bang": "!",
    "exclamation point": "!",
    "dollar": "$",
    "dollar sign": "$",
    "down score": "_",
    "under score": "_",
    "colon": ":",
    "paren": "(",
    "L paren": "(",
    "left paren": "(",
    "R paren": ")",
    "right paren": ")",
    "brace": "{",
    "left brace": "{",
    "R brace": "}",
    "right brace": "}",
    "angle": "<",
    "left angle": "<",
    "less than": "<",
    "rangle": ">",
    "R angle": ">",
    "right angle": ">",
    "greater than": ">",
    "star": "*",
    "asterisk": "*",
    "pound": "#",
    "hash": "#",
    "hash sign": "#",
    "number sign": "#",
    "percent": "%",
    "percent sign": "%",
    "caret": "^",
    "at sign": "@",
    "and sign": "&",
    "ampersand": "&",
    "amper": "&",
    "pipe": "|",
    "dubquote": '"',
    "double quote": '"',
}


ctx.lists["self.number_key"] = dict(zip(default_digits, numbers))
ctx.lists["self.arrow_key"] = {
    "down": "down",
    "left": "left",
    "right": "right",
    "up": "up",
}

simple_keys = [
    "end",
    "enter",
    "escape",
    "home",
    "insert",
    "pagedown",
    "pageup",
    "space",
    "tab",
]

alternate_keys = {
    "delete": "backspace",
    "forward delete": "delete",
    #'junk': 'backspace',
}
keys = {k: k for k in simple_keys}
keys.update(alternate_keys)
ctx.lists["self.special_key"] = keys
ctx.lists["self.function_key"] = {
    f"F {default_f_digits[i]}": f"f{i + 1}" for i in range(12)
}


@ctx.capture(rule="{self.modifier_key}+")
def modifiers(m):
    return "-".join(m.modifier_key_list)


@ctx.capture(rule="{self.arrow_key}")
def arrow_key(m) -> str:
    return m.arrow_key


@ctx.capture(rule="<self.arrow_key>+")
def arrow_keys(m) -> str:
    return str(m)


@ctx.capture(rule="{self.number_key}")
def number_key(m):
    return m.number_key


@ctx.capture(rule="{self.letter}")
def letter(m):
    return m.letter


@ctx.capture(rule="{self.special_key}")
def special_key(m):
    return m.special_key


@ctx.capture(rule="{self.symbol_key}")
def symbol_key(m):
    return m.symbol_key


@ctx.capture(rule="{self.function_key}")
def function_key(m):
    return m.function_key


@ctx.capture(
    rule="( <self.letter> | <self.number_key> | <self.symbol_key> "
         "| <self.arrow_key> | <self.function_key> | <self.special_key> )"
)
def unmodified_key(m) -> str:
    return str(m)


@ctx.capture(rule="{self.modifier_key}* <self.unmodified_key>")
def key(m) -> str:
    try:
        mods = m.modifier_key_list
    except AttributeError:
        mods = []
    return "-".join(mods + [m.unmodified_key])


@ctx.capture(rule="<self.key>+")
def keys(m) -> str:
    return " ".join(m.key_list)


@ctx.capture(rule="{self.letter}+")
def letters(m):
    return ''.join(m.letter_list)


@mod.action_class
class Actions:
    def get_alphabet() -> dict:
        """Provides the alphabet dictionary"""
        return alphabet

