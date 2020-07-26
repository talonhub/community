import os
import re
import time
from math import floor

from talon import Context, Module, actions, app, ui

ordinal_words = {}
ordinal_ones = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
    "ninth",
]
ordinal_teens = [
    "tenth",
    "eleventh",
    "twelfth",
    "thirteenth",
    "fourteenth",
    "fifteenth",
    "sixteenth",
    "seventeenth",
    "eighteenth",
    "nineteenth",
]
ordinal_tens = [
    "twentieth",
    "thirtieth",
    "fortieth",
    "fiftieth",
    "sixtieth",
    "seventieth",
    "eightieth",
    "ninetieth",
]
ordinal_tenty = [
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]


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
    ordinal_list = []
    if n > 19:
        if n % 10 == 0:
            ordinal_list.append(ordinal_tens[floor((n / 10)) - 2])
        else:
            ordinal_list.append(ordinal_tenty[floor(n / 10) - 2])
            ordinal_list.append(ordinal_ones[(n % 10) - 1])
    elif n > 9:
        ordinal_list.append(ordinal_teens[n - 11])
    else:
        ordinal_list.append(ordinal_ones[n - 1])

    result = " ".join(ordinal_list)
    return result


for n in range(1, 100):
    # This was initially minus one to compensate for its only use as a command
    # repeater, however ordinals themselves have other uses, so accommodating
    # the negative one in the command repeaters done in the actual talon file
    # now
    # ordinal_words[ordinal_word(n)] = n - 1
    ordinal_words[ordinal_word(n)] = n

mod = Module()
mod.list("ordinal_words", desc="list of ordinals")

ctx = Context()


@mod.capture
def ordinals(m) -> int:
    "Returns a single ordinial as a digit"


@ctx.capture(rule="{self.ordinal_words}")
def ordinals(m):
    o = m[0]
    return int(ordinal_words[o])


ctx.lists["self.ordinal_words"] = ordinal_words.keys()
