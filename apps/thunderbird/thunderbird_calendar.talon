app: thunderbird_calendar
-
# event/task
event new: user.thunderbird_mod("i")
task new: user.thunderbird_mod("d")
(task | event) delete: key(delete)
# layout
toggle today: key(f11)
view <number_small>: user.thunderbird_calendar_view(number_small)
view day: user.thunderbird_calendar_view(1)
view week: user.thunderbird_calendar_view(2)
view multi [week]: user.thunderbird_calendar_view(3)
view month: user.thunderbird_calendar_view(4)
