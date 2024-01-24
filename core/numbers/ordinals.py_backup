from talon import Context, Module


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


# The primitive ordinal words in English below a hundred.
ordinal_words = {
    0: "zeroth",
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh",
    8: "eighth",
    9: "ninth",
    10: "tenth",
    11: "eleventh",
    12: "twelfth",
    13: "thirteenth",
    14: "fourteenth",
    15: "fifteenth",
    16: "sixteenth",
    17: "seventeenth",
    18: "eighteenth",
    19: "nineteenth",
    20: "twentieth",
    30: "thirtieth",
    40: "fortieth",
    50: "fiftieth",
    60: "sixtieth",
    70: "seventieth",
    80: "eightieth",
    90: "ninetieth",
}
tens_words = "zero ten twenty thirty forty fifty sixty seventy eighty ninety".split()

# ordinal_numbers maps ordinal words into their corresponding numbers.
ordinal_numbers = {}
ordinal_small = {}
for n in range(1, 100):
    if n in ordinal_words:
        word = ordinal_words[n]
    else:
        (tens, units) = divmod(n, 10)
        assert 1 < tens < 10, "we have already handled all ordinals < 20"
        assert 0 < units, "we have already handled all ordinals divisible by ten"
        word = f"{tens_words[tens]} {ordinal_words[units]}"

    if n <= 20:
        ordinal_small[word] = n
    ordinal_numbers[word] = n


mod = Module()
ctx = Context()
mod.list("ordinals", desc="list of ordinals")
mod.list("ordinals_small", desc="list of ordinals small (1-20)")

ctx.lists["self.ordinals"] = ordinal_numbers.keys()
ctx.lists["self.ordinals_small"] = ordinal_small.keys()


@mod.capture(rule="{self.ordinals}")
def ordinals(m) -> int:
    """Returns a single ordinal as a digit"""
    return int(ordinal_numbers[m[0]])


@mod.capture(rule="{self.ordinals_small}")
def ordinals_small(m) -> int:
    """Returns a single ordinal as a digit"""
    return int(ordinal_numbers[m[0]])
