# Note: Dates are in US format (month[/day][/year])

# mm/0x
date <user.month> (o | zero) <digits>$:
	insert("{month}/0{digits}")

# mm/dd or mm/yy
date <user.month> <number_small>$:
	insert("{month}/{number_small}")

# mm/dd/0x
date <user.month> <user.day> (o | zero) <digits>$:
	insert("{month}/{day}/0{digits}")

# mm/dd/yy[yy]
date <user.month> <user.day> <user.year>:
	insert("{month}/{day}/{year}")

time <number_small> <user.ampm>:
	insert("{number_small}{ampm}")

time <number_small> <number> [<user.ampm>]:
	insert("{number_small}:{number}")
	insert(ampm or "")

time <number_small> [o] <digits> [<user.ampm>]:
	insert("{number_small}:0{digits}")
	insert(ampm or "")

time <number_small> o'clock [<user.ampm>]:
	insert("{number_small}:00")
	insert(ampm or "")

time <number_small> hundred:
	insert("{number_small}:00")

time one thousand:
	insert("10:00")

time two thousand:
	insert("20:00")

insert date:
	user.insert_date()

insert time:
	user.insert_time_ampm()

time stamp:
	user.insert_time_ampm()
	insert(" - ")