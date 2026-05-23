from datetime import date, timedelta
import calendar
from talon import Module, actions, settings

mod = Module()

# Declare lists in Talon grammar; values come from talon-list files
mod.list("month", "Month names and numeric values (1-12)")
mod.list("weekday", "Weekday names for relative date commands")

mod.setting("date_format", type=str, default="uk", desc="Preferred date format: uk, us, or iso")

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


def _format_with_preference(a_date: date) -> str:
    fmt = settings.get("user.date_format") or "uk"
    if fmt == "us":
        return a_date.strftime("%m/%d/%Y")
    if fmt == "iso":
        return a_date.strftime("%Y-%m-%d")
    # default UK
    return a_date.strftime("%d/%m/%Y")


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
        """Insert a formatted date from spoken day/month/year.

        `fmt` may be 'uk', 'us', 'iso', or `None` to use the user's
        `user.date_format` setting (default 'uk'). This function validates
        the calendar date and falls back to inserting a formatted string
        when the date is invalid.
        """
        day_num = int(day)
        month_num = _month_to_int(month)
        year_num = int(year)

        # Determine format preference
        fmt_pref = fmt or settings.get("user.date_format") or "uk"

        # Try to construct a real date for correct calendar handling
        try:
            computed = date(year_num, month_num, day_num)
            if fmt_pref == "us":
                actions.insert(computed.strftime("%m/%d/%Y"))
                return
            if fmt_pref == "iso":
                actions.insert(computed.strftime("%Y-%m-%d"))
                return
            # default UK
            actions.insert(computed.strftime("%d/%m/%Y"))
            return
        except ValueError:
            # Fall back to formatting by parts when invalid (e.g., 31 Feb)
            day_padded = f"{day_num:02d}"
            month_padded = f"{month_num:02d}"
            if fmt_pref == "us":
                date_str = f"{month_padded}/{day_padded}/{year_num}"
            elif fmt_pref == "iso":
                date_str = f"{year_num}-{month_padded}-{day_padded}"
            else:
                date_str = f"{day_padded}/{month_padded}/{year_num}"

            # Notify user that the spoken date was not a valid calendar date,
            # but still insert the best-effort formatted string.
            actions.app.notify(f"Invalid date spoken — inserted: {date_str}")
            actions.insert(date_str)

    def insert_date_formatted_iso(day: int, month: str, year: int):
        """Insert a formatted date from spoken day/month/year as yyyy-mm-dd"""
        day_padded = f"{int(day):02d}"
        month_padded = f"{_month_to_int(month):02d}"
        date_str = f"{year}-{month_padded}-{day_padded}"
        actions.insert(date_str)

    def insert_date_today():
        """Insert today according to preferred format"""
        actions.insert(_format_with_preference(date.today()))

    def insert_date_tomorrow():
        """Insert tomorrow according to preferred format"""
        actions.insert(_format_with_preference(date.today() + timedelta(days=1)))

    def insert_date_yesterday():
        """Insert yesterday according to preferred format"""
        actions.insert(_format_with_preference(date.today() - timedelta(days=1)))

    def insert_date_next_weekday(weekday: str):
        """Insert the next weekday name according to preferred format"""
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

    def insert_date_next_month():
        """Insert a date representing the same day next month"""
        today = date.today()
        year = today.year + (today.month // 12)
        month = today.month % 12 + 1
        day = min(today.day, calendar.monthrange(year, month)[1])
        next_month = date(year, month, day)
        actions.insert(_format_with_preference(next_month))

    def insert_date_next_year():
        """Insert a date representing the same day next year"""
        today = date.today()
        next_year = today.year + 1
        day = min(today.day, calendar.monthrange(next_year, today.month)[1])
        new_date = date(next_year, today.month, day)
        actions.insert(_format_with_preference(new_date))

    def insert_date_last_year():
        """Insert a date representing the same day last year"""
        today = date.today()
        last_year = today.year - 1
        day = min(today.day, calendar.monthrange(last_year, today.month)[1])
        new_date = date(last_year, today.month, day)
        actions.insert(_format_with_preference(new_date))

    def set_date_format_uk():
        """Set preferred date format to UK dd/mm/yyyy"""
        settings.set("user.date_format", "uk")

    def set_date_format_us():
        """Set preferred date format to US mm/dd/yyyy"""
        settings.set("user.date_format", "us")

    def set_date_format_iso():
        """Set preferred date format to ISO yyyy-mm-dd"""
        settings.set("user.date_format", "iso")





