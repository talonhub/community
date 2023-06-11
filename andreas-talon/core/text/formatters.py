from talon import Module, Context, actions
import re

mod = Module()
ctx = Context()


@mod.action_class
class Actions:

    def de_camel(text: str) -> str:
        """Replacing camelCase boundaries with blank space"""
        Ll = "a-zåäö"
        Lu = "A-ZÅÄÖ"
        L = f"{Ll}{Lu}"
        low_to_upper = rf"(?<=[{Ll}])(?=[{Lu}])"  # camel|Case
        upper_to_last_upper = rf"(?<=[L{Lu}])(?=[{Lu}][{Ll}])"  # IP|Address
        letter_to_digit = rf"(?<=[{L}])(?=[\d])"  # version|10
        digit_to_letter = rf"(?<=[\d])(?=[{L}])"  # 2|x
        return re.sub(
            rf"{low_to_upper}|{upper_to_last_upper}|{letter_to_digit}|{digit_to_letter}",
            " ",
            text,
        )


def format_delim(
    text,
    delimiter,
    format_first=None,
    format_rest=None,
):
    # Strip apostrophes and quotes
    text = re.sub(r"['`\"]+", "", text)
    # Split on anything that is not alpha-num
    words = re.split(r"([^\w\d]+)", text)
    groups = []
    group = []
    first = True

    for word in words:
        if not word.strip():
            continue
        # Word is number
        if bool(re.match(r"\d+", word)):
            first = True
        # Word is symbol
        elif bool(re.match(r"\W+", word)):
            groups.append(delimiter.join(group))
            word = word.strip()
            first = True
            groups.append(word)
            group = []
            continue
        elif first:
            first = False
            if format_first:
                word = format_first(word)
        elif format_rest:
            word = format_rest(word)
        group.append(word)

    groups.append(delimiter.join(group))
    return "".join(groups)


def first_and_rest(text, format_first=None, format_rest=None):
    words = text.split()

    for i, word in enumerate(words):
        if i == 0:
            if format_first:
                words[i] = format_first(word)
        elif format_rest:
            words[i] = format_rest(word)

    return " ".join(words) + get_trailing_whitespace(text)


def capitalize(text: str) -> str:
    return text.lower().capitalize()


def lower(text: str) -> str:
    return text.lower()


def upper(text: str) -> str:
    return text.upper()


def de_string(text: str) -> str:
    return text.strip('"').strip("'")


def get_trailing_whitespace(text: str) -> str:
    match = re.search(r"\s+$", text)
    return match.group() if match else ""
