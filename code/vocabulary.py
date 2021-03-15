from talon import Module, Context, resource
from typing import Dict, List, Tuple
import os
import csv
from pathlib import Path
from typing import Dict, List, Tuple

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="additional vocabulary words")


# NOTE: This method requires this module to be one folder below the top-level
#   knausj folder.
SETTINGS_DIR = Path(__file__).parents[1] / "settings"

if not SETTINGS_DIR.is_dir():
    os.mkdir(SETTINGS_DIR)

def get_list_from_csv(
    filename: str, headers: Tuple[str, str], default: Dict[str, str] = {}
):
    """Retrieves list from CSV"""
    path = SETTINGS_DIR / filename
    assert filename.endswith(".csv")

    if not path.is_file():
        with open(path, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for key, value in default.items():
                writer.writerow([key] if key == value else [value, key])

    # Now read via resource to take advantage of talon's
    # ability to reload this script for us when the resource changes
    with resource.open(str(path), "r") as f:
        rows = list(csv.reader(f))

    # print(str(rows))
    mapping = {}
    if len(rows) >= 2:
        actual_headers = rows[0]
        if not actual_headers == list(headers):
            print(
                f'"{filename}": Malformed headers - {actual_headers}.'
                + f" Should be {list(headers)}. Ignoring row."
            )
        for row in rows[1:]:
            if len(row) == 0:
                # Windows newlines are sometimes read as empty rows. :champagne:
                continue
            if len(row) == 1:
                output = spoken_form = row[0]
            else:
                output, spoken_form = row[:2]
                if len(row) > 2:
                    print(
                        f'"{filename}": More than two values in row: {row}.'
                        + " Ignoring the extras."
                    )
            # Leading/trailing whitespace in spoken form can prevent recognition.
            spoken_form = spoken_form.strip()
            mapping[spoken_form] = output

    return mapping

# Default words that will need to be capitalized (particularly under w2l).
# NB. These defaults and those later in this file are ONLY used when
# auto-creating the corresponding settings/*.csv files. Those csv files
# determine the contents of user.vocabulary and dictate.word_map. Once they
# exist, the contents of the lists/dictionaries below are irrelevant.
_capitalize_defaults = [
    "I",
    "I'm",
    "I've",
    "I'll",
    "I'd",
    "Monday",
    "Mondays",
    "Tuesday",
    "Tuesdays",
    "Wednesday",
    "Wednesdays",
    "Thursday",
    "Thursdays",
    "Friday",
    "Fridays",
    "Saturday",
    "Saturdays",
    "Sunday",
    "Sundays",
    "January",
    "February",
    # March omitted because it's a regular word too
    "April",
    # May omitted because it's a regular word too
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Default words that need to be remapped.
_word_map_defaults = {
    # E.g:
    # "cash": "cache",
}
_word_map_defaults.update({word.lower(): word for word in _capitalize_defaults})


# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.

ctx.settings["dictate.word_map"] = get_list_from_csv(
    "words_to_replace.csv",
    headers=("Replacement", "Original"),
    default=_word_map_defaults,
)


# Default words that should be added to Talon's vocabulary.
_simple_vocab_default = ["nmap", "admin", "Cisco", "Citrix", "VPN", "DNS", "Minecraft"]

# Defaults for different pronounciations of words that need to be added to
# Talon's vocabulary.
_default_vocabulary = {
    "N map": "nmap",
    "under documented": "under-documented",
}
_default_vocabulary.update({word: word for word in _simple_vocab_default})

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
ctx.lists["user.vocabulary"] = get_list_from_csv(
    "additional_words.csv",
    headers=("Word(s)", "Spoken Form (If Different)"),
    default=_default_vocabulary,
)
