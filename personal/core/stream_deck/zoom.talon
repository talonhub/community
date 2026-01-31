deck.serial: A00SA3232MA4OZ
-    
deck(zoom/left):
    tracking.zoom_cancel()
    mouse_click(0)
    user.zoom_clear_activated()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(zoom/right):
    tracking.zoom_cancel()
    mouse_click(1)
    user.zoom_clear_activated()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(zoom/double):
    tracking.zoom_cancel()
    mouse_click(0)
    mouse_click(0)
    user.zoom_clear_activated()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(zoom/triple):
    tracking.zoom_cancel()
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
    user.zoom_clear_activated()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(zoom/drag):
    tracking.zoom_cancel()
    user.mouse_drag(0)
    user.zoom_clear_activated()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(zoom/shift-left):
    key("shift:down")
    tracking.zoom_cancel()
    mouse_click(0)        
    key("shift:up")

    user.zoom_clear_activated()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")

deck(zoom/ctrl-left):
    key("ctrl:down")
    tracking.zoom_cancel()
    mouse_click(0)
    key("ctrl:up")
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")
    user.zoom_clear_activated()

deck(zoom/move):
    tracking.zoom_cancel()
    user.zoom_clear_activated()
    user.deck_set_cached_path_and_clear("A00SA3232MA4OZ")