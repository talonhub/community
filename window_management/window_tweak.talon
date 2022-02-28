
# show size and position information about the current window
window traits show:
    user.win_show()

# hide the window information window
window traits hide:
    user.win_hide()

# move the current window toward the center of the screen
window move:
    user.win_move()

# move the current window in the given direction
window move <user.compass_direction>:
    user.win_move(compass_direction)

# move the current window some percentage of its own size toward the center of the screen
window move <number> percent:
    user.win_move_percent(number)

# move the current window some percentage of its own size in the given direction
window move <user.compass_direction> <number> percent:
    user.win_move_percent(number, compass_direction)

# move the current window some number of pixels toward the center of the screen
window move <number_signed> pixels:
    user.win_move_pixels(number_signed)

# move the current window some number of pixels in the given direction
window move <user.compass_direction> <number_signed> pixels:
    user.win_move_pixels(number_signed, compass_direction)

# move the current window to the given coordinates (x at y)
window move <number_signed> at <number_signed>:
    user.win_move_absolute(number_signed_1, number_signed_2)

# move the current window so that the point indicated by the given direction is
# positioned at the given coordinates (x at y).
# Center means the window center, Northwest means the top left corner, East means
# the midpoint of the right-hand edge - like that all around.
window move <user.compass_direction> <number_signed> at <number_signed>:
    user.win_move_absolute(number_signed_1, number_signed_2, compass_direction)

# move the current window to the position indicated by the mouse pointer
window move to pointer:
    user.win_move_to_pointer()

# move the current window so that the point indicated by the given direction
# is positioned at the mouse pointer coordinates.
window move <user.compass_direction> to pointer:
    user.win_move_to_pointer(compass_direction)

# increase both the size and width of the current window simultaneously
window stretch:
    user.win_stretch()

# increase the size of the current window in the given direction
window stretch <user.compass_direction>:
    user.win_stretch(compass_direction)

# increase both the size and width of the current window by some percentage of its own size
window stretch <number> percent:
    user.win_resize_percent(number)

# increase the size of the current window by some percentage of its own size in the given direction
window stretch <user.compass_direction> <number> percent:
    user.win_resize_percent(number, compass_direction)

# increase both the size and width of the current window by some number of pixels
window stretch <number> pixels:
    user.win_resize_pixels(number)

# increase the size of the current window by some number of pixels in the given direction
window stretch <user.compass_direction> <number> pixels:
    user.win_resize_pixels(number, compass_direction)

# decrease both the size and width of the current window simultaneously
window shrink:
    user.win_shrink()

# decrease the size of the current window in the given direction
window shrink <user.compass_direction>:
    user.win_shrink(compass_direction)

# decrease both the size and width of the current window by some percentage of its own size
window shrink <number> percent:
    user.win_resize_percent(-1 * number)

# decrease the size of the current window by some percentage of its own size in the given direction
window shrink <user.compass_direction> <number> percent:
    user.win_resize_percent(-1 * number, compass_direction)

# decrease both the size and width of the current window by some number of pixels
window shrink <number> pixels:
    user.win_resize_pixels(-1 * number)

# decrease the size of the current window by some number of pixels in the given direction
window shrink <user.compass_direction> <number> pixels:
    user.win_resize_pixels(-1 * number, compass_direction)

# move current window to center of screen and adjust the size to some percentage of the screen size
window snap <number> percent [of screen]:
    user.win_snap_percent(number)

# change window size while keeping the center fixed
window size <number> by <number>:
    user.win_resize_absolute(number_1, number_2)

# change window size by stretching or shrinking in the given direction
window size <user.compass_direction> <number> by <number>:
    user.win_resize_absolute(number_1, number_2, compass_direction)

# stretch or shrink the current window to match the position indicated by the mouse pointer
# non_dual_direction is 'horizontal' or 'flat', 'vertical' or 'sharp', 'diagonal' or 'slant'
window size <user.non_dual_direction> to pointer:
    user.win_resize_to_pointer(non_dual_direction)

# restore current window's last remembered size and position
window revert:
    user.win_revert()
