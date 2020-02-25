from typing import Set

from talon import Module, Context, actions
import sys
    
default_alphabet = 'air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip'.split(' ')
letters = 'abcdefghijklmnopqrstuvwxyz'

default_digits = 'zero one two three four five six seven eight nine'.split(' ')
numbers = [str(i) for i in range(10)]

mod = Module()
mod.list('letter',   desc='The spoken phonetic alphabet')
mod.list('symbol',   desc='All symbols from the keyboard')
mod.list('arrow',    desc='All arrow keys')
mod.list('number',   desc='All number keys')
mod.list('modifier', desc='All modifier keys')
mod.list('special',  desc='All special keys')

@mod.capture
def modifiers(m) -> Set[str]:
    "One or more modifier keys"

@mod.capture
def arrow(m) -> str:
    "One directional arrow key"

@mod.capture
def arrows(m) -> str:
    "One or more arrows separate by a space"

@mod.capture
def number(m) -> str:
    "One number key"
 
@mod.capture
def letter(m) -> str:
    "One letter key" 

@mod.capture
def symbol(m) -> str:
    "One symbol key"

@mod.capture
def special(m) -> str:
    "One special key"

@mod.capture
def any(m) -> str:
    "Any one key"

@mod.capture
def key(m) -> str:
    "A single key with optional modifiers"

ctx = Context()
ctx.lists['self.modifier'] = {
    'command': 'cmd',
    'control': 'ctrl',   'troll':   'ctrl',
    'shift':   'shift',  'sky':     'shift',
    'alt':     'alt',    'option':  'alt',
    'super':   'super',
}

ctx.lists['self.letter'] = dict(zip(default_alphabet, letters))
ctx.lists['self.symbol'] = {
    'back tick': '`',
    'comma': ',',
    'dot': '.', 'period': '.',
    'semi': ';', 'semicolon': ';',
    'quote': "'",
    'L square': '[', 'left square': '[', 'square': '[',
    'R square': ']', 'right square': ']',
    'forward slash': '/', 'slash': '/',
    'backslash': '\\',
    'minus': '-', 'dash': '-',
    'equals': '=',
    'plus': '+',
    'question mark': '?',
    'tilde': '~',
    'bang': '!', 'exclamation point': '!', 
    'dollar': '$', 'dollar sign': '$',
    'down score': '_', 'under score': '_',
    'colon': ':',
    'paren': '(', 'L paren': '(', 'left paren': '(',
    'R paren': ')', 'right paren': ')',
    'brace': '{', 'left brace': '{',
    'R brace': '}', 'right brace': '}',
    'angle': '<', 'left angle': '<', 'less than': '<',
    'rangle': '>', 'R angle': '>', 'right angle': '>', 'greater than': '>',
    'star': '*', 'asterisk': '*',
    'pound': '#', 'hash': '#', 'hash sign': '#', 'number sign': '#',
    'percent': '%', 'percent sign': '%',
    'caret': '^',
    'at sign': '@',
    'and sign': '&', 'ampersand': '&', 'amper': '&',
    'pipe': '|',
    'dubquote': '"', 'double quote': '"',
}

ctx.lists['self.number'] = dict(zip(default_digits, numbers))
ctx.lists['self.arrow'] = {
    'left':  'left',
    'right': 'right',
    'up':    'up',
    'down':  'down',
}

simple_keys = [
    'tab', 'escape', 'enter', 'space',
    'home', 'pageup', 'pagedown', 'end',
]
alternate_keys = {
    'delete': 'backspace', 'junk': 'backspace',
    'forward delete': 'delete',
}
keys = {k: k for k in simple_keys}
keys.update(alternate_keys)
ctx.lists['self.special'] = keys

@ctx.capture(rule='{self.modifier}+')
def modifiers(m):
    return list(m.modifier)

@ctx.capture(rule='{self.arrow}')
def arrow(m) -> str:
    return m.arrow[0]

@ctx.capture(rule='<self.arrow>+')
def arrows(m) -> str: 
    return str(m)

@ctx.capture(rule='{self.number}')
def number(m):
    return m.number[0]

@ctx.capture(rule='{self.letter}')
def letter(m):
    return m.letter[0]

@ctx.capture(rule='{self.special}')
def special(m):
    return m.special[0]

@ctx.capture(rule='{self.symbol}')
def symbol(m):
    return m.symbol[0]
1
@ctx.capture(rule='(<self.arrow> | <self.number> | <self.letter> | <self.special>)')
def any(m) -> str: 
    return m._words[0]

@ctx.capture(rule='[<self.modifiers>] <self.any>')
def key(m) -> str:
    try:
        mods = m.modifiers
        return "-".join(mods + [m.any])
    except AttributeError:
        return m.any

@mod.action_class
class Actions:
    def key(m: str):
        """(TEMPORARY) Presses keys from captures defined in the keys.py module"""
        actions.key(m)

    def modifier_key(modifier: str, key: str):
        """(TEMPORARY) Presses the modifier plus supplied number"""
        res = "-".join([modifier] + [str(key)])
        actions.key(res)