from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("month", desc="months of the year")
mod.list("day", desc="calendar days (1st)")

@mod.capture(rule="{user.month} {user.day}")
def date(m) -> str:
    return f"{m.month} {m.day}"