tag: user.full_mouse_grid_showing

-

<user.letter> <user.letter> <number>:
    # say a letter to choose a row, say a second letter to choose a column, and say a number to choose the numbered block.  Example: "air bat 2"
    user.full_grid_input_partial(number)
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)


<user.letter> <user.letter>:
    # using the currently selected number block, say a letter to choose a row and say a second letter to choose a column. Example: "bat cap"
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)


<number> <user.letter> <user.letter>:
    # Say a number to select a number block, say a letter to select a row, and say a second leter to select a column. Example: "1 bat cap"
    user.full_grid_input_partial(number)
    user.full_grid_input_partial(letter_1)
    user.full_grid_input_partial(letter_2)

<number> <user.letter>: 
        user.full_grid_input_partial(number)
        user.full_grid_input_partial(letter)

^<number>$:
    # Say a number to select a number block. 
    user.full_grid_input_partial(number)

^horizontal <user.letter>$:
    #If you already have a row selected, saying 'horizontal' followed by a letter will select a new horizontal row.
    user.full_grid_input_horizontal(letter)

^<user.letter>$:
    #input a single letter. Depeing in where you are in the command sequence it will select either a row or a column.
    user.full_grid_input_partial(letter)

[dense] grid close:
    # close the grid. 
    user.full_grid_close()

checker grid:
    # change the overlay pattern to a checkerboard pattern.
    user.full_grid_checkers()

frame grid:
    # change the overlay pattern to a pattern where it is overlaid with frames.
    user.full_grid_frame()

phonetic grid: 
    # provides onscreen phonetic alphabet in rows and columns to make it so one does not have to remember the talon phonetic alphabet
    user.full_grid_phonetic()

full grid:
    # change the overlay pattern to overlay the screen with every possible number-letter-letter combination 
   user.full_grid_full()

darker letters:
    # Make the small letter labels more visible.
    user.full_grid_adjust_label_transparency(50)

lighter letters:
    # Make the small letter labels less visible.
    user.full_grid_adjust_label_transparency(-50)

darker background:
    # Make the large number blocks more visible.  
    user.full_grid_adjust_bg_transparency(20)

lighter background:
    #Make the large number blocks less visible. 
    user.full_grid_adjust_bg_transparency(-20)

bigger grid: 
    # Make the grid blocks larger.
    user.full_grid_adjust_size(5)

smaller grid: 
    # Make the grib blocks smaller. 
    user.full_grid_adjust_size(-5)


