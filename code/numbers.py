from talon import Context, Module, actions

digits = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
teens = [
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
tens = [
    "ten",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]
scales = [
    "hundred",
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
    "sextillion",
    "septillion",
    "octillion",
    "nonillion",
    "decillion",
]

digits_map = {n: i for i, n in enumerate(digits)}
teens_map = {n: i + 11 for i, n in enumerate(teens)}
tens_map = {n: 10 * (i + 1) for i, n in enumerate(tens)}
digits_map["oh"] = 0

scales_map = {scales[0]: 100}
scales_map.update({n: 10 ** ((i + 1) * 3) for i, n in enumerate(scales[1:])})

alt_digits = "(" + ("|".join(digits_map.keys())) + ")"
alt_teens = "(" + ("|".join(teens_map.keys())) + ")"
alt_tens = "(" + ("|".join(tens_map.keys())) + ")"
alt_scales = "(" + ("|".join(scales_map.keys())) + ")"

# fuse scales (hundred, thousand) leftward onto numbers (one, twelve, twenty, etc)
def fuse_scale(words, limit=None):
    ret = []
    n = None
    scale = 1
    for w in words:
        if w in tens_map:
            scale *= tens_map[w]
            continue
        elif w in scales_map and (limit is None or scales_map[w] < limit):
            scale *= scales_map[w]
            continue
        elif w == "and":
            continue

        if n is not None:
            ret.append(n * scale)
        n = None
        scale = 1

        if isinstance(w, int):
            n = w
        else:
            ret.append(w)

    if n is not None:
        ret.append(n * scale)
    return ret


# fuse small numbers leftward onto larger numbers
def fuse_num(words):
    ret = []
    acc = None
    sig = 0
    for w in words:
        if isinstance(w, int):
            if acc is None:
                acc = w
                sig = 10 ** len(str(w))
            elif acc > w:
                nsig = 10 ** len(str(w))
                if nsig >= sig:
                    acc *= nsig
                acc += w
                sig = min(sig, nsig)
            else:
                ret.append(acc)
                acc = w
                sig = 0
        else:
            if acc is not None:
                ret.append(acc)
                acc = None
                sig = 0
            ret.append(w)
    if acc is not None:
        ret.append(acc)
    return ret


"""
def test_num(n):
    print('testing', n)
    step1 = fuse_scale(list(n), 1000)
    step2 = fuse_num(step1)
    step3 = fuse_scale(step2)
    step4 = fuse_num(step3)
    print('step1', step1)
    print('step2', step2)
    print('step3', step3)
    print('step4', step4)
    return step4[0]
assert(test_num([1, 'hundred', 'thousand', 'and', 5, 'thousand', 'and', 6, 'thousand']) == 1050006000)
assert(test_num([1, 'hundred', 'and', 5, 'thousand']) == 105000)
assert(test_num([1, 'thousand', 'thousand']) == 1000000)
assert(test_num([1, 'million', 5, 'hundred', 1, 'thousand']) == 1501000)
assert(test_num([1, 'million', 5, 'hundred', 'and', 1, 'thousand', 1, 'hundred', 'and', 6]) == 1501106)
assert(test_num([1, 'million', 1, 1]) == 10000011)
assert(test_num([1, 'million', 10, 10]) == 100001010)
"""

ctx = Context()


@ctx.capture("digits", rule=f"{alt_digits}+")
def digits(m):
    return int("".join([str(digits_map[n]) for n in m]))


@ctx.capture(
    "number_small", rule=f"({alt_digits} | {alt_teens} | {alt_tens} [{alt_digits}])"
)
def number_small(m):
    result = 0
    for word in m:
        if word in digits_map:
            result += digits_map[word]
        elif word in tens_map:
            result += tens_map[word]
        elif word in teens_map:
            result += teens_map[word]
    return result


@ctx.capture(
    "self.number_scaled",
    rule=f"<number_small> [{alt_scales} ([and] (<number_small> | {alt_scales} | <number_small> {alt_scales}))*]",
)
def number_scaled(m):
    return fuse_num(fuse_scale(fuse_num(fuse_scale(list(m), 1000))))[0]


# This rule offers more colloquial number speaking when combined with a command
# like: "go to line <number>"
# Example: " one one five            " == 115
#          " one fifteen             " == 115
#          " one hundred and fifteen " == 115
@ctx.capture("number", rule=f"(<digits> | [<digits>] <user.number_scaled>)")
def number(m):
    return int("".join(str(i) for i in list(m)))


@ctx.capture("number_signed", rule=f"[negative] <number>")
def number_signed(m):
    number = m[-1]
    if m[0] == "negative":
        return -number
    return number


mod = Module()
mod.list("number_scaled", desc="Mix of numbers and digits")


@mod.capture
def number_scaled(m) -> str:
    "Returns a series of numbers as a string"
