
# show size and position information about the current window
win show$:
    user.win_show()

# hide the window information window
win hide$:
    user.win_hide()

# move the current window toward the center of the screen
win move$:
    user.win_move()

# move the current window in the given direction
win move <user.compass_direction>$:
    user.win_move(compass_direction)

# move the current window some percentage of its own size toward the center of the screen
win move <number> percent$:
    user.win_move_percent(number)
    
# move the current window some percentage of its own size in the given direction
win move <user.compass_direction> <number> percent$:
    user.win_move_percent(number, compass_direction)

# move the current window some number of pixels toward the center of the screen
win move <number_signed> pixels$:
    user.win_move_pixels(number_signed)
    
# move the current window some number of pixels in the given direction
win move <user.compass_direction> <number_signed> pixels$:
    user.win_move_pixels(number_signed, compass_direction)

# move the current window to the given coordinates (x at y)
win move <number_signed> at <number_signed>$:
    user.win_move_absolute(number_signed_1, number_signed_2)

# move the current window so that the point indicated by the given direction is
# positioned at the given coordinates (x at y).
# Center means the window center, Northwest means the top left corner, East means
# the midpoint of the right-hand edge - like that all around.
win move <user.compass_direction> <number_signed> at <number_signed>$:
    user.win_move_absolute(number_signed_1, number_signed_2, compass_direction)

# increase both the size and width of the current window simultaneously
win stretch$:
    user.win_stretch()

# increase the size of the current window in the given direction
win stretch <user.compass_direction>$:
    user.win_stretch(compass_direction)

# increase both the size and width of the current window by some percentage of its own size 
win stretch <number> percent$:
    user.win_resize_percent(number)

# increase the size of the current window by some percentage of its own size in the given direction
win stretch <user.compass_direction> <number> percent$:
    user.win_resize_percent(number, compass_direction)

# increase both the size and width of the current window by some number of pixels
win stretch <number> pixels$:
    user.win_resize_pixels(number)

# increase the size of the current window by some number of pixels in the given direction
win stretch <user.compass_direction> <number> pixels$:
    user.win_resize_pixels(number, compass_direction)

# decrease both the size and width of the current window simultaneously
win shrink$:
    user.win_shrink()

# decrease the size of the current window in the given direction
win shrink <user.compass_direction>$:
    user.win_shrink(compass_direction)

# decrease both the size and width of the current window by some percentage of its own size 
win shrink <number> percent$:
    user.win_resize_percent(-1 * number)

# decrease the size of the current window by some percentage of its own size in the given direction
win shrink <user.compass_direction> <number> percent$:
    user.win_resize_percent(-1 * number, compass_direction)

# decrease both the size and width of the current window by some number of pixels
win shrink <number> pixels$:
    user.win_resize_pixels(-1 * number)
    
# decrease the size of the current window by some number of pixels in the given direction
win shrink <user.compass_direction> <number> pixels$:
    user.win_resize_pixels(-1 * number, compass_direction)

# move current window to center of screen and adjust the size to some percentage of the screen size 
win snap <number> percent [of screen]$:
    user.win_snap_percent(number)

# change window size while keeping the center fixed
win size <number> by <number>$:
    user.win_resize_absolute(number_1, number_2)

# change window size by stretching or shrinking in the given direction
win size <user.compass_direction> <number> by <number>$:
    user.win_resize_absolute(number_1, number_2, compass_direction)

# restore current window's last remembered size and position
win revert$:
    user.win_revert()
