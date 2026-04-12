deck.serial: A00SA3232MA4OZ
-    
deck(gaze/left):
    tracking.zoom_cancel()
    mouse_click(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/right):
    tracking.zoom_cancel()
    mouse_click(1)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/double):
    tracking.zoom_cancel()
    mouse_click(0)
    mouse_click(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/triple):
    tracking.zoom_cancel()
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/drag):
    tracking.zoom_cancel()
    user.mouse_drag(0)
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/shift-left):
    key("shift:down")
    tracking.zoom_cancel()
    mouse_click(0)        
    key("shift:up")

    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/ctrl-left):
    key("ctrl:down")
    tracking.zoom_cancel()
    mouse_click(0)
    key("ctrl:up")
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(gaze/move):
    tracking.zoom_cancel()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")