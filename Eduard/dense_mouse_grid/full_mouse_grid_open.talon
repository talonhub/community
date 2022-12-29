tag: user.full_mouse_grid_showing
and tag: user.full_mouse_grid_enabled
and mode: user.full_mouse_grid
and not mode: sleep

-

<user.letter> <user.letter> <number>:
    user.full_grid_input_partial(number)
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)
    user.full_grid_close()

<user.letter> <user.letter> <number> {user.mg_point_of_compass}:
    user.full_grid_input_partial(number)
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)

    user.full_grid_close()

<user.letter> <user.letter> {user.mg_point_of_compass}:
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)
    user.full_grid_close()

<user.letter> <user.letter>:
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)
    user.full_grid_close()

<number> <user.letter> <user.letter>:
    user.full_grid_input_partial(number)
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)
    user.full_grid_close()

^<number>$:
    user.full_grid_input_partial(number)

^horizontal <user.letter>$:
    user.full_grid_input_horizontal(letter)

^<user.letter>$:
    user.full_grid_input_partial(letter)

close:
    user.full_grid_close()

alphabet checkers:
    user.full_grid_checkers()

alphabet frame:
    user.full_grid_frame()

alphabet full: 
   user.full_grid_full()

alphabet rulers:
    user.full_grid_rulers_toggle()

add noodles:
    user.full_grid_adjust_label_transparency(50)

eat noodles:
    user.full_grid_adjust_label_transparency(-50)

thicker broth:
    user.full_grid_adjust_bg_transparency(50)

thinner broth:
    user.full_grid_adjust_bg_transparency(-50)

what the [heck | fuck]:
    app.notify("say alphabet close to get rid of the alphabet soup")



touch: 
    mouse_click(0)

#If you want to be able to say random things without remembering to put talon to sleep, uncomment this command
#<user.prose>: skip()
    