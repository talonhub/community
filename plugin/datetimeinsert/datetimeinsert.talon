settings():
    # Define the default date format for all date commands using Python strftime codes.
    # Use an explicit pattern to avoid ambiguous locale output.
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    user.date_format = "%m-%d-%Y"

date insert:
    user.deprecate_command("2026-05-10", "date insert", "date today")
    insert(user.time_format("%Y-%m-%d"))

date insert UTC:
    user.deprecate_command("2026-05-10", "date insert UTC", "date today UTC")
    insert(user.time_format_utc("%Y-%m-%d"))

date today UTC: insert(user.time_format_utc("%Y-%m-%d"))

timestamp insert: insert(user.time_format("%Y-%m-%d %H:%M:%S"))
timestamp insert high resolution: insert(user.time_format("%Y-%m-%d %H:%M:%S.%f"))
timestamp insert UTC: insert(user.time_format_utc("%Y-%m-%d %H:%M:%S"))
timestamp insert UTC high resolution:
    insert(user.time_format_utc("%Y-%m-%d %H:%M:%S.%f"))

# Date entry commands using day, month, year lists

# Insert date using the configured default format from settings.
# Example command: 'date 31 January 2026'
date {user.day} {user.month} <number>: user.insert_date_from_parts(day, month, number)

# Insert a date using an explicit strftime pattern.
# Example: 'date 31 January 2026 %Y-%m-%d'
date {user.day} {user.month} <number> format:
    user.insert_date_formatted(day, month, number, format)

# Relative date commands
# Today/now uses the configured default format from settings.
date (today | now): user.insert_date_today()

# Relative day modifiers
date tomorrow: user.insert_date_relative(1, 0, 0)
date yesterday: user.insert_date_relative(-1, 0, 0)

# Relative month/year
date next month: user.insert_date_relative(0, 1, 0)
date last month: user.insert_date_relative(0, -1, 0)
date next year: user.insert_date_relative(0, 0, 1)
date last year: user.insert_date_relative(0, 0, -1)

# Next weekday Example: 'date next Wednesday'
# (weekday list defined in weekdays.talon-list)
date next {user.weekday}$: user.insert_date_next_weekday(weekday)
