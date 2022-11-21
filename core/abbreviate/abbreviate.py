# XXX - would be nice to be able pipe these through formatters

from talon import Context, Module

from ..user_settings import get_list_from_csv

mod = Module()
mod.list("abbreviation", desc="Common abbreviation")

ctx = Context()

abbreviations = get_list_from_csv(
    "abbreviations.csv", headers=("Word", "Abbreviation"), dir="."
)
ctx.lists["user.abbreviation"] = abbreviations
