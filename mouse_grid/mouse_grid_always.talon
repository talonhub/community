mouse grid:
    user.grid_select_screen(1)
    user.grid_activate()

grid win:
    user.grid_place_window()
    user.grid_activate()

grid <user.number_key>+:
    user.grid_activate()
    user.grid_narrow_list(number_key_list)

grid screen [<number>]:
    user.grid_select_screen(number or 1)
    user.grid_activate()
