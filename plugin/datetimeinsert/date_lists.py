from datetime import date, timedelta
import calendar
from talon import Context, Module, actions, settings

from core.numbers.numbers import get_spoken_form_under_one_hundred

mod = Module()
ctx = Context()

# Declare lists in Talon grammar; values come from talon-list files
mod.list("month", "Month names and numeric values (1-12)")
mod.list("day", "Days of the month, 1-31")
mod.list("weekday", "Weekday names for relative date commands")
ctx.lists["user.day"] = get_spoken_form_under_one_hundred(
    1,
    31,
    include_oh_variant_for_single_digits=False,
    include_default_variant_for_single_digits=True,
)
# Date format using standard (1989 C standard) format codes.
# Default to a full-year ISO-like representation to avoid ambiguous locale output.
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
mod.setting("date_format", type=str, default="%Y-%m-%d", desc="Preferred date format (using format codes)")

WEEKDAY_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

MONTH_MAP = {
    **{name.lower(): i for i, name in enumerate(calendar.month_name) if name},
    **{name.lower(): i for i, name in enumerate(calendar.month_abbr) if name},
    "sept": 9,
}


def _resolve_date_format(fmt: str | None) -> str:
    """Return the configured format or a concrete strftime pattern."""
    return fmt or settings.get("user.date_format") or "%Y-%m-%d"


def _format_with_preference(a_date: date) -> str:
    fmt = _resolve_date_format(None)
    return a_date.strftime(fmt)  # default to locale


def _month_to_int(month) -> int:
    """Convert a spoken month (name, abbreviation, or numeric string/int) to its month number.

    Accepts ints, numeric strings, full month names ("january"), and abbreviations ("jan").
    """
    if isinstance(month, int):
        return month
    m = str(month).strip().lower()
    if m.isdigit():
        return int(m)
    # Use module-level MONTH_MAP to avoid rebuilding mappings every call
    if m in MONTH_MAP:
        return MONTH_MAP[m]
    raise ValueError(f"Unknown month: {month}")


@mod.action_class
class Actions:
    def insert_date_from_parts(day: int, month: str, year: int):
        """Insert date from spoken day/month/year using preferred date_format."""
        actions.user.insert_date_formatted(day, month, year, None)

    def insert_date_formatted(day: int, month: str, year: int, fmt: str = None):
        """Insert a date from spoken day/month/year using `strftime` format codes.

        `fmt` may be a concrete format string such as `%Y-%m-%d` or `%d-%m-%Y`.
        When omitted, this uses the user's `user.date_format` setting. The
        function validates the date before inserting it.
        """
        day_num = int(day)
        month_num = _month_to_int(month)
        year_num = int(year)

        fmt_pref = _resolve_date_format(fmt)

        # Try to construct a real date for correct calendar handling
        try:
            computed = date(year_num, month_num, day_num)
            actions.insert(computed.strftime(fmt_pref))
            return
        except ValueError:
            # Invalid Date Received (e.g., 31 Feb)
            actions.app.notify(f"Invalid date spoken — could not insert: {day_num}/{month_num}/{year_num}")

    def insert_date_formatted_iso(day: int, month: str, year: int):
        """Insert a date from spoken day/month/year using the ISO `%Y-%m-%d` format."""
        actions.user.insert_date_formatted(day, month, year, "%Y-%m-%d")

    def insert_date_today():
        """Insert today according to preferred format"""
        actions.insert(_format_with_preference(date.today()))
    
    def insert_date_relative(days: int, months: int, years: int):
        """Insert a date relative to today by the specified number of days, months, and years."""
        today = date.today()
        # Calculate the new year and month
        new_year = today.year + years
        new_month = today.month + months
        # Adjust year and month if new_month is out of bounds
        while new_month > 12:
            new_month -= 12
            new_year += 1
        while new_month < 1:
            new_month += 12
            new_year -= 1
        # Calculate the last day of the new month to avoid invalid dates
        last_day_of_new_month = calendar.monthrange(new_year, new_month)[1]
        # Ensure the day does not exceed the last day of the new month
        new_day = min(today.day, last_day_of_new_month)
        # Create the new date and add the relative days
        relative_date = date(new_year, new_month, new_day) + timedelta(days=days)
        actions.insert(_format_with_preference(relative_date))

    def insert_date_first_of_month():
        """Insert the first day of the current month."""
        today = date.today()
        actions.insert(_format_with_preference(date(today.year, today.month, 1)))

    def insert_date_last_day_of_month():
        """Insert the last day of the current month."""
        today = date.today()
        last_day = calendar.monthrange(today.year, today.month)[1]
        actions.insert(_format_with_preference(date(today.year, today.month, last_day)))

    def insert_date_next_weekday(weekday: str):
        """Insert the next occurrence of a weekday according to preferred format."""
        weekday_norm = weekday.strip().lower()
        if weekday_norm not in WEEKDAY_MAP:
            raise ValueError(f"Unknown weekday: {weekday}")
        target = WEEKDAY_MAP[weekday_norm]
        today = date.today()
        days_ahead = (target - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        next_day = today + timedelta(days=days_ahead)
        actions.insert(_format_with_preference(next_day))

    def insert_date_last_weekday(weekday: str):
        """Insert the previous occurrence of a weekday according to preferred format."""
        weekday_norm = weekday.strip().lower()
        if weekday_norm not in WEEKDAY_MAP:
            raise ValueError(f"Unknown weekday: {weekday}")
        target = WEEKDAY_MAP[weekday_norm]
        today = date.today()
        days_ago = (today.weekday() - target + 7) % 7
        if days_ago == 0:
            days_ago = 7
        last_day = today - timedelta(days=days_ago)
        actions.insert(_format_with_preference(last_day))
