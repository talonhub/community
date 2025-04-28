tag: user.splits
-

# Note: The verb "to split" (the process) and the noun "the split" (the result)
# logically refer to different axes:
#
#                     |
#                     |
#                     |
# --------------------+--------------------
#      Splitting along|the hor. axis...
#                     |
#                     | ...creates
#                     | a split along
#                     | the vert. axis.
#
# This is why the phrase "split vertically" to create a vertical split would be
# incorrect, because it implies that "split" is a verb. With "split vertical" - when
# accepting the different word order as is customary in this repository - "split" can be
# understood as a noun - just like in "split clear" - and is thus correctly referring to
# the resulting split line. This way, we have accurate phrases that still harmonize with
# general software conventions.
#
# In phrases like "split right" on the other hand, "split" has to be understood as a
# verb, because, in this case, it means "to the right" (horizontal axis), creating a
# split line on the other, the vertical axis.

split right: user.split_window_right()
split left: user.split_window_left()
split down: user.split_window_down()
split up: user.split_window_up()
split (vertical | why): user.split_window_vertical_line()
split (horizontal | ex): user.split_window_horizontal_line()
split flip: user.split_flip()
split max: user.split_maximize()
split reset: user.split_reset()
split window: user.split_window()
split clear: user.split_clear()
split clear all: user.split_clear_all()
split next: user.split_next()
split last: user.split_last()
go split <number>: user.split_number(number)
