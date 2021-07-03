from dataclasses import dataclass
from typing import Dict, Generic, List, Mapping, Optional, TypeVar
from collections import defaultdict
import itertools

from talon import actions, registry
from talon import Context, Module, app, imgui, ui, fs
import re

from .extensions import file_extensions
from .numbers import digits_map
from .abbreviate import abbreviations
from .keys import symbol_key_words

mod = Module()

# TODO: 'Whats application': 'WhatsApp' (Should keep "whats app" as well?)
# TODO: 'V O X': 'VOX' (should keep "VOX" as well?)
# Could handle by handling all alternatives for these, or by having hardcoded list of things that we want to handle specially

DEFAULT_MINIMUM_TERM_LENGTH = 3

SMALL_WORD = r"[A-Z]?[a-z]+"
# TODO: We want "AXEvery" to be ["AX", "Every"]
UPPERCASE_WORD = r"[A-Z]+"
FILE_EXTENSIONS_REGEX = "|".join(
    re.escape(file_extension.strip()) for file_extension in file_extensions.values()
)
DIGITS_REGEX = r"\d"
SYMBOLS_REGEX = "|".join(re.escape(symbol) for symbol in set(symbol_key_words.values()))
FULL_REGEX_NO_SYMBOLS = re.compile(
    "|".join([DIGITS_REGEX, FILE_EXTENSIONS_REGEX, SMALL_WORD, UPPERCASE_WORD,])
)
FULL_REGEX = re.compile(
    "|".join(
        [DIGITS_REGEX, FILE_EXTENSIONS_REGEX, SMALL_WORD, UPPERCASE_WORD, SYMBOLS_REGEX]
    )
)

REVERSE_PRONUNCIATION_MAP = {
    **{value: key for key, value in abbreviations.items()},
    **{value.strip(): key for key, value in file_extensions.items()},
    **{str(value): key for key, value in digits_map.items()},
    **{value: key for key, value in symbol_key_words.items()},
}


def create_single_spoken_form(source: str):
    normalized_source = source.lower()
    try:
        mapped_source = REVERSE_PRONUNCIATION_MAP[normalized_source]
    except KeyError:
        mapped_source = source
    if mapped_source.isupper():
        mapped_source = " ".join(mapped_source)
    return mapped_source


T = TypeVar("T")


@dataclass
class SpeakableItem(Generic[T]):
    name: str
    value: T


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

        pieces_no_symbols = list(FULL_REGEX_NO_SYMBOLS.finditer(source))

        pieces_with_symbols = list(FULL_REGEX.finditer(source))

        spoken_form_with_symbols = " ".join(
            [create_single_spoken_form(piece.group(0)) for piece in pieces_with_symbols]
        ).lower()

        spoken_form_without_symbols = " ".join(
            [create_single_spoken_form(piece.group(0)) for piece in pieces_no_symbols]
        ).lower()

        # these two may be identical, so ensure the list is reduced
        full_forms = list(
            set(
                [spoken_form_with_symbols.lower(), spoken_form_without_symbols.lower(),]
            )
        )

        # only generate the subsequences if requested
        if generate_subsequences:
            term_sequence = spoken_form_without_symbols.split(" ")
            terms = list(
                {
                    term.lower().strip()
                    for term in (
                        term_sequence
                        + list(
                            itertools.accumulate([f"{term} " for term in term_sequence])
                        )
                    )
                }
            )

            # add the full form if not present
            if spoken_form_with_symbols not in terms:
                terms.append(spoken_form_with_symbols)

        else:
            terms = full_forms

        terms = [
            term
            for term in terms
            if (term not in words_to_exclude and len(term) >= minimum_term_length)
            # always keep the full forms, even if < min term length?
            or term in full_forms
        ]

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
        sources: Mapping[str, T],
        words_to_exclude: Optional[List[str]] = None,
        minimum_term_length: int = DEFAULT_MINIMUM_TERM_LENGTH,
        generate_subsequences: bool = True,
    ) -> Dict[str, T]:
        """Create spoken forms for all sources in a map, doing conflict resolution"""
        all_spoken_forms: defaultdict[str, List[SpeakableItem[T]]] = defaultdict(list)

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
