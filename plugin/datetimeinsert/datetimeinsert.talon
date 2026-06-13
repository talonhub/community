settings():
    # Define the date format mode for all date commands: %x (locale's preferred date representation) | uk | us | iso
    user.date_format = "%x"

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

# Insert date using preferred mode from settings
^date {user.day} {user.month} <number>$: user.insert_date_from_parts(day, month, number)

# Insert date as US format mm/dd/yyyy
# (defaults remains dd/mm/yyyy for standard use)
^date {user.day} {user.month} <number> us$:
    user.insert_date_formatted_us(day, month, number)

# Insert date as ISO format yyyy-mm-dd
^date {user.day} {user.month} <number> iso$:
    user.insert_date_formatted_iso(day, month, number)

# Relative date commands
# Today/now uses list default or settings format
^date today$: user.insert_date_today()
^date now$: user.insert_date_today()

# Relative day modifiers
^date tomorrow$: user.insert_date_tomorrow()
^date yesterday$: user.insert_date_yesterday()

# Relative month/year
^date next month$: user.insert_date_next_month()
^date next year$: user.insert_date_next_year()
^date last year$: user.insert_date_last_year()

# Next weekday
# (weekday list defined in weekdays.talon-list)
^date next {user.weekday}$: user.insert_date_next_weekday(weekday)
