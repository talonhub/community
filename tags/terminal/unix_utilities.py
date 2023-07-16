from talon import Context, Module

from ...core.user_settings import get_list_from_csv

ctx = Context()
mod = Module()

mod.tag(
    "unix_utilities", desc="tag for enabling unix utility commands in your terminal"
)

mod.list("unix_utility", desc="A common utility command")
