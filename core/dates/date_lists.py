from datetime import date, timedelta
import calendar
from talon import Module, actions, settings

mod = Module()

# Declare lists in Talon grammar; values come from talon-list files
mod.list("day", "Ordinal and numeric day values (1-31)")
mod.list("month", "Month names and numeric values (1-12)")
mod.list("year", "Year values from 1964 to 2066")
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


def _format_with_preference(a_date: date) -> str:
    fmt = settings.get("user.date_format") or "uk"
    if fmt == "us":
        return a_date.strftime("%m/%d/%Y")
    if fmt == "iso":
        return a_date.strftime("%Y-%m-%d")
    if fmt != "uk":
        # Notify on invalid configuration but still fall back to UK format
        try:
            actions.app.notify(
                f"Invalid user.date_format '{fmt}' (expected 'uk', 'us', or 'iso'); falling back to 'uk'."
            )
        except Exception:
            # If notification fails for any reason, silently fall back to UK
            pass
    # default UK
    return a_date.strftime("%d/%m/%Y")


@mod.action_class
class Actions:
    def insert_date_from_parts(day: str, month: str, year: str):
        """Insert date from spoken day/month/year using preferred date_format"""
        day_padded = day.zfill(2)
        month_padded = month.zfill(2)
        try:
            year_num = int(year)
            month_num = int(month_padded)
            day_num = int(day_padded)
            computed = date(year_num, month_num, day_num)
        except ValueError:
            # Invalid combination of day/month/year (e.g., "thirty first" "february").
            actions.app.notify(f"Invalid date: {day}/{month}/{year}")
            return
        actions.insert(_format_with_preference(computed))

    def insert_date_formatted(day: str, month: str, year: str):
        """Insert a formatted date from spoken day/month/year as dd/mm/yyyy"""
        day_padded = day.zfill(2)
        month_padded = month.zfill(2)
        date_str = f"{day_padded}/{month_padded}/{year}"
        actions.insert(date_str)

    def insert_date_formatted_us(day: str, month: str, year: str):
        """Insert a formatted date from spoken day/month/year as mm/dd/yyyy"""
        day_padded = day.zfill(2)
        month_padded = month.zfill(2)
        date_str = f"{month_padded}/{day_padded}/{year}"
        actions.insert(date_str)

    def insert_date_formatted_iso(day: str, month: str, year: str):
        """Insert a formatted date from spoken day/month/year as yyyy-mm-dd"""
        day_padded = day.zfill(2)
        month_padded = month.zfill(2)
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
        """Insert the date of the next occurrence of the given weekday according to preferred format"""
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





