# Date entry commands using day, month, year lists

# Insert date using preferred mode from settings
date {user.day} {user.month} {user.year}:
    user.insert_date_from_parts(day, month, year)

# Insert date as US format mm/dd/yyyy
# (default remains dd/mm/yyyy for standard use)
date {user.day} {user.month} {user.year} us:
    user.insert_date_formatted_us(day, month, year)

# Insert date as ISO format yyyy-mm-dd
date {user.day} {user.month} {user.year} iso:
    user.insert_date_formatted_iso(day, month, year)

# Relative date commands
# Today/now uses list default or settings format
date today: user.insert_date_today()
date now: user.insert_date_today()

# Relative day modifiers
date tomorrow: user.insert_date_tomorrow()
date yesterday: user.insert_date_yesterday()

# Relative month/year
date next month: user.insert_date_next_month()
date next year: user.insert_date_next_year()
date last year: user.insert_date_last_year()

# Next weekday
# (weekday list defined in weekdays.talon-list)
date next {user.weekday}: user.insert_date_next_weekday(weekday)
