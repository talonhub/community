import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from talon import Module, actions

from .abbreviate.abbreviate import abbreviations_list
from .file_extension.file_extension import file_extensions
from .keys.keys import symbol_key_words
from .numbers.numbers import digits_map, scales, teens, tens

mod = Module()


DEFAULT_MINIMUM_TERM_LENGTH = 2
EXPLODE_MAX_LEN = 3
FANCY_REGULAR_EXPRESSION = r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|[0-9]+"
FILE_EXTENSIONS_REGEX = "|".join(
    re.escape(file_extension.strip()) + "$"
    for file_extension in file_extensions.values()
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
twenties = ["", ""] + list(tens)
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
        # Leave completely uppercase words alone, as we can deal with them later.
        # Otherwise normalized the rest to help with subsequent abbreviation lookups,
        # etc.
        if source.isupper():
            mapped_source = source
        else:
            mapped_source = source.lower()
    return mapped_source


def create_exploded_forms(spoken_forms: List[str]):
    """Exploded common packed words into separate words"""
    # TODO: This could be moved somewhere else, possibly seeded from something like
    # words to replace...
    packed_words = {"readme": "read me"}

    new_spoken_forms = []
    for line in spoken_forms:
        exploded_form = []
        # ex: "vm" or "usb" explodes into "V M" or "U S B"

        if (
            " " not in line
            and line.islower()
            and len(line) > 1
            and len(line) <= EXPLODE_MAX_LEN
        ):
            new_spoken_forms.append(line)  # Keep a regular copy (ie: "nas")
            new_spoken_forms.append(" ".join(line.upper()))
        # ex: "readme" explodes into "read me"
        else:
            for word in line.split(" "):
                if word in packed_words.keys():
                    exploded_form.append(packed_words[word])
                else:
                    exploded_form.append(word)
            new_spoken_forms.append(" ".join(exploded_form))
    return new_spoken_forms


def create_extension_forms(spoken_forms: List[str]):
    """Add extension forms"""
    new_spoken_forms = []

    file_extensions_map = {v.strip(): k for k, v in file_extensions.items()}
    for line in spoken_forms:
        have_file_extension = False
        file_extension_forms = []
        dotted_extension_form = []
        truncated_forms = []
        for substring in line.split(" "):
            # NOTE: If we ever run in to file extensions in the middle of file name, the
            # truncated form is going to be busted. ie: foo.md.disabled

            if substring in file_extensions_map.keys():
                file_extension_forms.append(file_extensions_map[substring])
                dotted_extension_form.append(REVERSE_PRONUNCIATION_MAP["."])
                dotted_extension_form.append(file_extensions_map[substring])
                have_file_extension = True
                # purposefully down update truncated
            else:
                file_extension_forms.append(substring)
                dotted_extension_form.append(substring)
                truncated_forms.append(substring)
        # print(file_extension_forms)
        if have_file_extension:
            new_spoken_forms.append(" ".join(file_extension_forms))
            new_spoken_forms.append(" ".join(dotted_extension_form))
        new_spoken_forms.append(" ".join(truncated_forms))

    return set(dict.fromkeys(new_spoken_forms))


def create_cased_forms(spoken_forms: List[str]):
    """Add lower and upper case forms"""
    new_spoken_forms = []

    for line in spoken_forms:
        lower_forms = []
        upper_forms = []
        # print(line)
        for substring in line.split(" "):
            if substring.isupper():
                lower_forms.append(substring.lower())
                upper_forms.append(" ".join(substring))
            else:
                lower_forms.append(substring)
                upper_forms.append(substring)

        new_spoken_forms.append(" ".join(lower_forms))
        new_spoken_forms.append(" ".join(upper_forms))

    return set(dict.fromkeys(new_spoken_forms))


def create_abbreviated_forms(spoken_forms: List[str]):
    """Add abbreviated case forms"""
    new_spoken_forms = []

    swapped_abbreviation_map = {v: k for k, v in abbreviations_list.items()}
    for line in spoken_forms:
        unabbreviated_forms = []
        abbreviated_forms = []
        for substring in line.split(" "):
            if substring in swapped_abbreviation_map.keys():
                abbreviated_forms.append(swapped_abbreviation_map[substring])
            else:
                abbreviated_forms.append(substring)
            unabbreviated_forms.append(substring)

        new_spoken_forms.append(" ".join(abbreviated_forms))
        new_spoken_forms.append(" ".join(unabbreviated_forms))

    return set(dict.fromkeys(new_spoken_forms))


def create_spoken_number_forms(source: List[str]):
    """
    Create a list of spoken forms by transforming numbers in source into spoken forms.
    This creates a first pass of spoken forms with numbers translated, but will go
    through multiple other passes.
    """

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

    for substring in source:
        # for piece in pieces:
        # substring = piece.group(0)
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
            full_form_digit_wise.append(spoken_form)
            full_form_fancy_numbers.append(spoken_form)
            full_form_spoken_form_years.append(spoken_form)

    if has_fancy_number_version:
        spoken_forms.append(" ".join(full_form_fancy_numbers))

    if has_spoken_form_years:
        result = " ".join(full_form_spoken_form_years)
        if result not in spoken_forms:
            spoken_forms.append(result)

    spoken_forms.append(" ".join(full_form_digit_wise))
    return set(dict.fromkeys(spoken_forms))


def create_spoken_forms_from_regex(source: str, pattern: re.Pattern):
    """
    Creates a list of spoken forms for source using the provided regex pattern.
    For numeric pieces detected by the regex, generates both digit-wise and full
    spoken forms for the numbers where appropriate.
    """
    pieces = list(pattern.finditer(source))
    spoken_forms = list(map(lambda x: x.group(0), pieces))

    # NOTE: Order is sometimes important
    transforms = [
        create_spoken_number_forms,
        create_extension_forms,
        create_cased_forms,
        create_exploded_forms,
        create_abbreviated_forms,
        create_extension_forms,
    ]

    for func in transforms:
        spoken_forms = func(spoken_forms)

    return list(dict.fromkeys(spoken_forms))


def generate_string_subsequences(
    source: str,
    words_to_exclude: list[str],
    minimum_term_length: int,
):
    # Includes (lower-cased):
    # 1. Each word in source, eg "foo bar baz" -> "foo", "bar", "baz".
    # 2. Each leading subsequence of words from source,
    #    eg "foo bar baz" -> "foo", "foo bar", "foo bar baz"
    #    (but not "bar baz" - TODO: is this intentional?)
    #
    # Except for:
    # 3. strings shorter than minimum_term_length
    # 4. strings in words_to_exclude.
    term_sequence = source.split(" ")
    terms = {
        # WARNING: This .lower() version creates unwanted duplication of broken up
        # uppercase words, eg 'R E A D M E' -> 'r e a d m e'. Everything else should be
        # lower case already
        # term.lower().strip()
        term.strip()
        for term in (
            term_sequence
            + list(itertools.accumulate([f"{term} " for term in term_sequence]))
        )
    }
    return [
        term
        for term in terms
        if (term not in words_to_exclude and len(term) >= minimum_term_length)
    ]


@dataclass
class SpeakableItem:
    name: str
    value: Any


@mod.action_class
class Actions:
    def create_spoken_forms(
        source: str,
        words_to_exclude: Optional[list[str]] = None,
        minimum_term_length: int = DEFAULT_MINIMUM_TERM_LENGTH,
        generate_subsequences: bool = True,
    ) -> list[str]:
        """Create spoken forms for a given source"""

        spoken_forms_without_symbols = create_spoken_forms_from_regex(
            source, REGEX_NO_SYMBOLS
        )

        # todo: this could probably be optimized out if there's no symbols
        spoken_forms_with_symbols = create_spoken_forms_from_regex(
            source, REGEX_WITH_SYMBOLS
        )

        # some may be identical, so ensure the list is reduced
        spoken_forms = set(spoken_forms_with_symbols + spoken_forms_without_symbols)

        # only generate the subsequences if requested
        if generate_subsequences:
            # todo: do we care about the subsequences that are excluded.
            # the only one that seems relevant are the full spoken form for
            spoken_forms.update(
                generate_string_subsequences(
                    spoken_forms_without_symbols[-1],
                    words_to_exclude or [],
                    minimum_term_length,
                )
            )

        # Avoid empty spoken forms.
        return [x for x in spoken_forms if x]

    def create_spoken_forms_from_list(
        sources: list[str],
        words_to_exclude: Optional[list[str]] = None,
        minimum_term_length: int = DEFAULT_MINIMUM_TERM_LENGTH,
        generate_subsequences: bool = True,
    ) -> dict[str, str]:
        """Create spoken forms for all sources in a list, doing conflict resolution"""
        return actions.user.create_spoken_forms_from_map(
            {source: source for source in sources},
            words_to_exclude,
            minimum_term_length,
            generate_subsequences,
        )

    def create_spoken_forms_from_map(
        sources: Mapping[str, Any],
        words_to_exclude: Optional[list[str]] = None,
        minimum_term_length: int = DEFAULT_MINIMUM_TERM_LENGTH,
        generate_subsequences: bool = True,
    ) -> dict[str, Any]:
        """Create spoken forms for all sources in a map, doing conflict resolution"""
        all_spoken_forms: defaultdict[str, list[SpeakableItem]] = defaultdict(list)

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
