from talon import Context, Module
from .user_settings import get_list_from_csv

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="additional vocabulary words")

# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.

ctx.settings["dictate.word_map"] = get_list_from_csv(
    "words_to_replace.csv", headers=("Replacement", "Original"),
)


# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
ctx.lists["user.vocabulary"] = get_list_from_csv(
    "additional_words.csv", headers=("Word(s)", "Spoken Form (If Different)"),
)

# for quick verification of the reload
# print(str(ctx.settings["dictate.word_map"]))
# print(str(ctx.lists["user.vocabulary"]))
