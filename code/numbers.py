from typing import Iterator, Union

from talon import Context, Module

mod = Module()
ctx = Context()

digits = "zero one two three four five six seven eight nine".split()
teens = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
tens = "twenty thirty forty fifty sixty seventy eighty ninety".split()
scales = "hundred thousand million billion trillion quadrillion quintillion sextillion septillion octillion nonillion decillion".split()

digits_map = {n: i for i, n in enumerate(digits)}
digits_map["oh"] = 0
teens_map = {n: i + 10 for i, n in enumerate(teens)}
tens_map = {n: 10 * (i + 2) for i, n in enumerate(tens)}
scales_map = {n: 10 ** (3 * (i + 1)) for i, n in enumerate(scales[1:])}
scales_map["hundred"] = 100

numbers_map = digits_map.copy()
numbers_map.update(teens_map)
numbers_map.update(tens_map)
numbers_map.update(scales_map)


def parse_number(l: list[str]) -> str:
    """Parses a list of words into a number/digit string."""
    l = list(scan_small_numbers(l))
    for scale in scales:
        l = parse_scale(scale, l)
    return "".join(str(n) for n in l)


def scan_small_numbers(l: list[str]) -> Iterator[Union[str, int]]:
    """
    Takes a list of number words, yields a generator of mixed numbers & strings.
    Translates small number terms (<100) into corresponding numbers.
    Drops all occurrences of "and".
    Smashes digits onto tens words, eg. ["twenty", "one"] -> [21].
    But note that "ten" and "zero" are excluded, ie:
      ["ten", "three"] -> [10, 3]
      ["fifty", "zero"] -> [50, 0]
    Does nothing to scale words ("hundred", "thousand", "million", etc).
    """
    # reversed so that repeated pop() visits in left-to-right order
    l = [x for x in reversed(l) if x != "and"]
    while l:
        n = l.pop()
        # fuse tens onto digits, eg. "twenty", "one" -> 21
        if n in tens_map and l and digits_map.get(l[-1], 0) != 0:
            d = l.pop()
            yield numbers_map[n] + numbers_map[d]
        # turn small number terms into corresponding numbers
        elif n not in scales_map:
            yield numbers_map[n]
        else:
            yield n


def parse_scale(scale: str, l: list[Union[str, int]]) -> list[Union[str, int]]:
    """Parses a list of mixed numbers & strings for occurrences of the following
    pattern:

        <multiplier> <scale> <remainder>

    where <scale> is a scale word like "hundred", "thousand", "million", etc and
    multiplier and remainder are numbers or strings of numbers of the
    appropriate size. For example:

        parse_scale("hundred", [1, "hundred", 2]) -> [102]
        parse_scale("thousand", [12, "thousand", 3, 45]) -> [12345]

    We assume that all scales of lower magnitude have already been parsed; don't
    call parse_scale("thousand") until you've called parse_scale("hundred").
    """
    scale_value = scales_map[scale]
    scale_digits = len(str(scale_value))

    # Split the list on the desired scale word, then parse from left to right.
    left, *splits = split_list(scale, l)
    for right in splits:
        # (1) Figure out the multiplier by looking to the left of the scale
        # word. We ignore non-integers because they are scale words that we
        # haven't processed yet; this strategy means that "thousand hundred"
        # gets parsed as 1,100 instead of 100,000, but "hundred thousand" is
        # parsed correctly as 100,000.
        before = 1  # default multiplier
        if left and isinstance(left[-1], int) and left[-1] != 0:
            before = left.pop()

        # (2) Absorb numbers to the right, eg. in [1, "thousand", 1, 26], "1
        # thousand" absorbs ["1", "26"] to make 1,126. We pull numbers off
        # `right` until we fill up the desired number of digits.
        after = ""
        while right and isinstance(right[0], int):
            next = after + str(right[0])
            if len(next) >= scale_digits:
                break
            after = next
            right.pop(0)
        after = int(after) if after else 0

        # (3) Push the parsed number into place, append whatever was left
        # unparsed, and continue.
        left.append(before * scale_value + after)
        left.extend(right)

    return left


def split_list(value, l: list) -> Iterator:
    """Splits a list by occurrences of a given value."""
    start = 0
    while True:
        try:
            i = l.index(value, start)
        except ValueError:
            break
        yield l[start:i]
        start = i + 1
    yield l[start:]


# # ---------- TESTS (uncomment to run) ----------
# def test_number(expected, string):
#     print('testing:', string)
#     l = list(scan_small_numbers(string.split()))
#     print("  scan --->", l)
#     for scale in scales:
#         old = l
#         l = parse_scale(scale, l)
#         if scale in old: print("  parse -->", l)
#         else: assert old == l, "parse_scale should do nothing if the scale does not occur in the list"
#     result = "".join(str(n) for n in l)
#     assert result == parse_number(string.split())
#     assert str(expected) == result, f"parsing {string!r}, expected {expected}, got {result}"

# test_number(105000, "one hundred and five thousand")
# test_number(1000000, "one thousand thousand")
# test_number(1501000, "one million five hundred one thousand")
# test_number(1501106, "one million five hundred and one thousand one hundred and six")
# test_number(123, "one two three")
# test_number(123, "one twenty three")
# test_number(104, "ten four") # borderline, but valid in some dialects
# test_number(1066, "ten sixty six") # a common way of saying years
# test_number(1906, "nineteen oh six") # year
# test_number(2001, "twenty oh one") # year
# test_number(2020, "twenty twenty")
# test_number(1001, "one thousand one")
# test_number(1010, "one thousand ten")
# test_number(123456, "one hundred and twenty three thousand and four hundred and fifty six")
# test_number(123456, "one twenty three thousand four fifty six")

# ## failing (and somewhat debatable) tests from old numbers.py
# #test_number(10000011, "one million one one")
# #test_number(100001010, "one million ten ten")
# #test_number(1050006000, "one hundred thousand and five thousand and six thousand")


# ---------- CAPTURES ----------
alt_digits = "(" + "|".join(digits_map.keys()) + ")"
alt_teens = "(" + "|".join(teens_map.keys()) + ")"
alt_tens = "(" + "|".join(tens_map.keys()) + ")"
alt_scales = "(" + "|".join(scales_map.keys()) + ")"
number_word = "(" + "|".join(numbers_map.keys()) + ")"
# don't allow numbers to start with scale words like "hundred", "thousand", etc
leading_words = numbers_map.keys() - scales_map.keys()
leading_words -= {"oh", "o"}  # comment out to enable bare/initial "oh"
number_word_leading = f"({'|'.join(leading_words)})"

# TODO: allow things like "double eight" for 88
@ctx.capture("digit_string", rule=f"({alt_digits} | {alt_teens} | {alt_tens})+")
def digit_string(m) -> str:
    return parse_number(list(m))


@ctx.capture("digits", rule="<digit_string>")
def digits(m) -> int:
    """Parses a phrase representing a digit sequence, returning it as an integer."""
    return int(m.digit_string)


@mod.capture(rule=f"{number_word_leading} ([and] {number_word})*")
def number_string(m) -> str:
    """Parses a number phrase, returning that number as a string."""
    return parse_number(list(m))


@ctx.capture("number", rule="<user.number_string>")
def number(m) -> int:
    """Parses a number phrase, returning it as an integer."""
    return int(m.number_string)


@ctx.capture("number_signed", rule=f"[negative|minus] <number>")
def number_signed(m):
    number = m[-1]
    return -number if (m[0] in ["negative", "minus"]) else number


@ctx.capture(
    "number_small", rule=f"({alt_digits} | {alt_teens} | {alt_tens} [{alt_digits}])"
)
def number_small(m):
    return int(parse_number(list(m)))
