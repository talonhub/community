from dataclasses import dataclass
from typing import Dict, Generic, List, Mapping, Optional, TypeVar, Any
from collections import defaultdict
import itertools

from talon import actions
from talon import Module
import re

from .extensions import file_extensions
from .numbers import digits_map, teens, scales, tens
from .abbreviate import abbreviations
from .keys import symbol_key_words

mod = Module()


# TODO: 'Whats application': 'WhatsApp' (Should keep "whats app" as well?)
# TODO: 'V O X': 'VOX' (should keep "VOX" as well?)
# Could handle by handling all alternatives for these, or by having hardcoded list of things that we want to handle specially
# TODO: Tests
DEFAULT_MINIMUM_TERM_LENGTH = 3
FANCY_REGULAR_EXPRESSION = r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|[0-9]+"
FILE_EXTENSIONS_REGEX = "|".join(
    re.escape(file_extension.strip()) + "$" for file_extension in file_extensions.values()
)
SYMBOLS_REGEX = "|".join(re.escape(symbol) for symbol in set(symbol_key_words.values()))
REGEX_NO_SYMBOLS = re.compile(
    "|".join(
        [
            FANCY_REGULAR_EXPRESSION,
            FILE_EXTENSIONS_REGEX,
        ]
    )
)

REGEX_WITH_SYMBOLS = re.compile(
    "|".join([FANCY_REGULAR_EXPRESSION, FILE_EXTENSIONS_REGEX, SYMBOLS_REGEX])
)

REVERSE_PRONUNCIATION_MAP = {
    **{value: key for key, value in abbreviations.items()},
    **{value.strip(): key for key, value in file_extensions.items()},
    **{str(value): key for key, value in digits_map.items()},
    **{value: key for key, value in symbol_key_words.items()},
}

# begin: create the lists etc necessary for create_spoken_word_for_number
# by convention, each entry in the list has an append space... until I clean up the function
# the algorithm's expectation is slightly different from numbers.py

# ["", "one ", "two ",... "nine "] or equivalents
ones = [""] + [
    REVERSE_PRONUNCIATION_MAP[str(index)] for index in range(10) if index != 0
]

# ["","","twenty","thirty","forty",..."ninety"]
# or equivalent
twenties = ["", ""] + [val for val in tens]
# print("twenties = " + str(twenties))

thousands = [""] + [val for index, val in enumerate(scales) if index != 0]
# print("thousands = " + thousands)
# end: create the lists necessary for create_spoken_word_for_number


def create_spoken_form_for_number(num: int):
    """Creates a spoken form for an integer"""

    n3 = []
    r1 = ""
    # create numeric string
    ns = str(num)
    for k in range(3, 33, 3):
        r = ns[-k:]
        q = len(ns) - k
        # break if end of ns has been reached
        if q < -2:
            break
        else:
            if q >= 0:
                n3.append(int(r[:3]))
            elif q >= -1:
                n3.append(int(r[:2]))
            elif q >= -2:
                n3.append(int(r[:1]))
        r1 = r

    # break each group of 3 digits into
    # ones, tens/twenties, hundreds
    words = []
    for i, x in enumerate(n3):
        b1 = x % 10
        b2 = (x % 100) // 10
        b3 = (x % 1000) // 100
        if x == 0:
            continue  # skip
        else:
            t = thousands[i]

        # print(str(b1) + ", " + str(b2) + ", " + str(b3))
        if b2 == 0:
            words = [ones[b1], t] + words
        elif b2 == 1:
            words = [teens[b1], t] + words
        elif b2 > 1:
            words = [twenties[b2], ones[b1], t] + words
        if b3 > 0:
            words = [ones[b3], scales[0]] + words

    # filter out the empty strings and join
    return " ".join(filter(None, words))


def create_spoken_form_years(num: str):
    """Creates spoken forms for numbers 1000 <= num <= 9999. Returns None if not supported"""

    val = int(num)
    if val > 9999 or val < 1000:
        return None

    centuries = val // 100
    remainder = val % 100

    words = []

    if centuries % 10 != 0:
        words.append(create_spoken_form_for_number(centuries))

        # 1900 -> nineteen hundred
        if remainder == 0:
            words.append(scales[0])
    else:

        # 200X -> two thousand x
        if remainder < 9:
            words.append(REVERSE_PRONUNCIATION_MAP[str(centuries // 10)])
            words.append(scales[1])

        # 20XX => twenty xx
        else:
            words.append(create_spoken_form_for_number(str(centuries)))

    if remainder != 0:
        # 1906 => "nineteen six"
        if remainder < 10:

            # todo: decide if we want nineteen oh five"
            # todo: decide if we want "and"
            # both seem like a waste
            # if centuries % 10 != 0:
            #     words.append("oh")

            words.append(REVERSE_PRONUNCIATION_MAP[str(remainder)])
        else:
            words.append(create_spoken_form_for_number(remainder))

    return " ".join(words)


# # ---------- create_spoken_form_years  (uncomment to run) ----------
# def test_year(year: str, expected: str):
#     result = create_spoken_form_years(year)
#     print(f"test_year: test string = {year}, result = {result}, expected = {expected}")
#     assert create_spoken_form_years(year) == expected


# print("************* test_year tests ******************")
# test_year("1100", "eleven hundred")
# test_year("1905", "nineteen five")
# test_year("1910", "nineteen ten")
# test_year("1925", "nineteen twenty five")
# test_year("2000", "two thousand")
# test_year("2005", "two thousand five")
# test_year("2020", "twenty twenty")
# test_year("2019", "twenty nineteen")
# test_year("2085", "twenty eighty five")
# test_year("2100", "twenty one hundred")
# test_year("2105", "twenty one five")
# test_year("9999", "ninety nine ninety nine")
# print("************* test_year tests done**************")


def create_single_spoken_form(source: str):
    """
    Returns a spoken form of a string
        (1) Returns the value from REVERSE_PRONUNCIATION_MAP if it exists
        (2) Splits allcaps into separate letters ("ABC" -> A B C)
        (3) Otherwise, returns the lower case source.
    """
    normalized_source = source.lower()

    try:
        mapped_source = REVERSE_PRONUNCIATION_MAP[normalized_source]
    except KeyError:
        mapped_source = source
    if mapped_source.isupper():
        mapped_source = " ".join(mapped_source)
    return mapped_source


def create_spoken_forms_from_regex(source: str, pattern: re.Pattern):
    """
    Creates a list of spoken forms for source using the provided regex pattern.
    For numeric pieces detected by the regex, generates both digit-wise and full
    spoken forms for the numbers where appropriate.
    """
    pieces = list(pattern.finditer(source))

    # list of spoken forms returned
    spoken_forms = []

    # contains the pieces for the spoken form with individual digits
    full_form_digit_wise = []

    # contains the pieces for the spoken form with the spoken version of the number
    full_form_fancy_numbers = []

    # contains the pieces for the spoken form for years like "1900" => nineteen hundred
    full_form_spoken_form_years = []

    # indicates whether or not we processed created a version with the full number (>10) translated
    has_fancy_number_version = False

    # indicates whether or not we processed created a version with the year-like ("1900" => nineteen hundred) numbers
    has_spoken_form_years = False
    # print(source)
    for piece in pieces:
        substring = piece.group(0)
        length = len(substring)

        # the length is currently capped at 31 digits
        if length > 1 and length <= 31 and substring.isnumeric():
            has_fancy_number_version = True
            val = int(substring)
            spoken_form_years = create_spoken_form_years(val)
            spoken_form = create_spoken_form_for_number(val)

            if spoken_form_years:
                has_spoken_form_years = True
                full_form_spoken_form_years.append(spoken_form_years)
            else:
                full_form_spoken_form_years.append(spoken_form)

            full_form_fancy_numbers.append(spoken_form)

            # build the serial digit version
            for digit in substring:
                full_form_digit_wise.append(create_single_spoken_form(digit))

        else:
            spoken_form = create_single_spoken_form(substring)
            full_form_fancy_numbers.append(spoken_form)
            full_form_spoken_form_years.append(spoken_form)
            full_form_digit_wise.append(spoken_form)

    if has_fancy_number_version:
        spoken_forms.append(" ".join(full_form_fancy_numbers).lower())

    if has_spoken_form_years:
        result = " ".join(full_form_spoken_form_years)
        if result not in spoken_forms:
            spoken_forms.append(result)

    spoken_forms.append(" ".join(full_form_digit_wise).lower())

    return spoken_forms


def generate_string_subsequences(
    source: str,
    words_to_exclude: List[str],
    minimum_term_length=DEFAULT_MINIMUM_TERM_LENGTH,
):
    term_sequence = source.split(" ")
    terms = list(
        {
            term.lower().strip()
            for term in (
                term_sequence
                + list(itertools.accumulate([f"{term} " for term in term_sequence]))
            )
        }
    )

    terms = [
        term
        for term in terms
        if (term not in words_to_exclude and len(term) >= minimum_term_length)
    ]

    return terms


@dataclass
class SpeakableItem:
    name: str
    value: Any


@mod.action_class
class Actions:
    def create_spoken_forms(
        source: str,
        words_to_exclude: Optional[List[str]] = None,
        minimum_term_length: int = DEFAULT_MINIMUM_TERM_LENGTH,
        generate_subsequences: bool = True,
    ) -> List[str]:
        """Create spoken forms for a given source"""

        if words_to_exclude is None:
            words_to_exclude = []

        spoken_forms_without_symbols = create_spoken_forms_from_regex(
            source, REGEX_NO_SYMBOLS
        )

        # todo: this could probably be optimized out if there's no symbols
        spoken_forms_with_symbols = create_spoken_forms_from_regex(
            source, REGEX_WITH_SYMBOLS
        )

        # some may be identical, so ensure the list is reduced
        full_spoken_forms = list(
            set(spoken_forms_with_symbols + spoken_forms_without_symbols)
        )

        # only generate the subsequences if requested
        if generate_subsequences:

            # todo: do we care about the subsequences that are excluded.
            # the only one that seems relevant are the full spoken form for
            terms = generate_string_subsequences(
                spoken_forms_without_symbols[-1], words_to_exclude, minimum_term_length
            )

            # always keep the full terms... there's probably a better way to do this
            for form in full_spoken_forms:
                if form not in terms:
                    terms.append(form)

        else:
            terms = full_spoken_forms

        return terms

    def create_spoken_forms_from_list(
        sources: List[str],
        words_to_exclude: Optional[List[str]] = None,
        minimum_term_length: int = DEFAULT_MINIMUM_TERM_LENGTH,
        generate_subsequences: bool = True,
    ) -> Dict[str, str]:
        """Create spoken forms for all sources in a list, doing conflict resolution"""
        return actions.user.create_spoken_forms_from_map(
            {source: source for source in sources},
            words_to_exclude,
            minimum_term_length,
            generate_subsequences,
        )

    def create_spoken_forms_from_map(
        sources: Mapping[str, Any],
        words_to_exclude: Optional[List[str]] = None,
        minimum_term_length: int = DEFAULT_MINIMUM_TERM_LENGTH,
        generate_subsequences: bool = True,
    ) -> Dict[str, Any]:
        """Create spoken forms for all sources in a map, doing conflict resolution"""
        all_spoken_forms: defaultdict[str, List[SpeakableItem]] = defaultdict(list)

        for name, value in sources.items():
            spoken_forms = actions.user.create_spoken_forms(
                name, words_to_exclude, minimum_term_length, generate_subsequences
            )
            for spoken_form in spoken_forms:
                all_spoken_forms[spoken_form].append(SpeakableItem(name, value))

        final_spoken_forms = {}
        for spoken_form, spoken_form_sources in all_spoken_forms.items():
            if len(spoken_form_sources) > 1:
                final_spoken_forms[spoken_form] = min(
                    spoken_form_sources,
                    key=lambda speakable_item: len(speakable_item.name),
                ).value
            else:
                final_spoken_forms[spoken_form] = spoken_form_sources[0].value

        return final_spoken_forms
