from talon import app, Module, Context, actions, ui
import re
import time
import os
import platform
from math import floor

ordinal_words = {}
ordinal_ones = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eight', 'ninth']
ordinal_teens = ['tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth']
ordinal_tens = ['twentieth', 'thirtieth', 'fortieth', 'fiftieth', 'sixtieth', 'seventieth', 'eightieth', 'ninetieth']
ordinal_tenty = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

def ordinal(n):
    """
    Convert an integer into its ordinal representation::
        ordinal(0)   => '0th'
        ordinal(3)   => '3rd'
        ordinal(122) => '122nd'
        ordinal(213) => '213th'
    """
    n = int(n)
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    return str(n) + suffix

def ordinal_word(n):
    n = int(n)
    result = ""
    if n > 19:
        if n % 10 == 0:
            result += ordinal_tens[floor((n / 10)) - 2]
        else:
            result += ordinal_tenty[floor(n / 10) - 2]
            result += ordinal_ones[(n % 10) - 1]
    elif n > 9:
        result += ordinal_teens[n - 11]
    else:
        result += ordinal_ones[n - 1]
    return result

for n in range(2, 100):
    ordinal_words[ordinal_word(n)] = n - 1

mod = Module()
mod.list('ordinal_words', desc='list of ordinals')

ctx = Context()
@mod.capture
def ordinals(m) -> int:
    "Returns a single ordinial as a digit"
    
@ctx.capture(rule='{self.ordinal_words}')
def ordinals(m):
    o = m[0]
    return int(ordinal_words[o])

ctx.lists['self.ordinal_words'] = ordinal_words.keys()
    



