from talon import Context, Module
from contextlib import suppress

mod = Module()
ctx = Context()

mod.list("month", desc="months of the year")
mod.list("day", desc="calendar days (1st)")
mod.list("year", desc="calendar year")

month_to_digits = { "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "vovember": 11, "december": 12 }

@mod.capture(rule="({user.month} {user.day} [{user.year}])")
def date_written(m) -> str:
    year = None
    month = None
    day = None

    with suppress(AttributeError):
        year =  m.year

    if year:
        return f"{m.month} {m.day}, {year}"
    else:
        return f"{m.month} {m.day}"
    

@mod.capture(rule="date {user.month} {user.day} [{user.year}]")
def date_numeric(m) -> str:
    year = None
    
    with suppress(AttributeError):
        year =  m.year

    if year:
        return f"{month_to_digits[m.month.lower()]}/{m.day[:-2]}/{year}"
    else:
        return f"{month_to_digits[m.month.lower()]}/{m.day[:-2]}"
    
@mod.capture(rule="<user.date_numeric> | <user.date_written> | {user.year}")
def date(m) -> str:
    return str(m)