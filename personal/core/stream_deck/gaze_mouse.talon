deck.serial: A00SA3232MA4OZ
-    
deck(gaze/zoom):
    user.gaze_grid_narrow_at_cursor()

deck(gaze/left):
    user.gaze_grid_toggle()
    mouse_click(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/right):
    user.gaze_grid_toggle()
    mouse_click(1)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/double):
    user.gaze_grid_toggle()
    mouse_click(0)
    mouse_click(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/triple):
    user.gaze_grid_toggle()
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/drag):
    user.gaze_grid_toggle()
    user.mouse_drag(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/shift-left):
    key("shift:down")
    user.gaze_grid_toggle()
    mouse_click(0)        
    key("shift:up")

    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/ctrl-left):
    key("ctrl:down")
    user.gaze_grid_toggle()
    mouse_click(0)
    key("ctrl:up")
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/move):
    user.gaze_grid_toggle()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")