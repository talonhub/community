not tag: user.homerow_search
not tag: user.fluent_search_screen_search
not tag: user.homerow_search
not tag: user.clickable_overlay_active
-
zoom mouse: user.mouse_toggle_zoom_mouse()
control mouse: user.mouse_toggle_control_mouse()
    

run calibration: tracking.calibrate()

touch$:
    # close zoom if open
    tracking.zoom_cancel()

    mouse_click(0)
    # close the mouse grid if open
    user.grid_close()
    # End any open drags
    # Touch automatically ends left drags so this is for right drags specifically
    user.mouse_drag_end()

^connie$:
    # close zoom if open
    tracking.zoom_cancel()

    mouse_click(1)
    # close the mouse grid if open
    user.grid_close()

# mid click:
    # close zoom if open
    tracking.zoom_cancel()

#     mouse_click(2)
#     # close the mouse grid
#     user.grid_close()

# #see keys.py for modifiers.
# #defaults
# #command
# #control
# #option = alt
# #shift
# #super = windows key
<user.modifiers> touch:
    # close zoom if open
    tracking.zoom_cancel()

    key("{modifiers}:down")
    mouse_click(0)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
<user.modifiers> connie:
    # close zoom if open
    tracking.zoom_cancel()

    key("{modifiers}:down")
    mouse_click(1)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
(duke)$:
    # close zoom if open
    tracking.zoom_cancel()

    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
(ripple)$:
    # close zoom if open
    tracking.zoom_cancel()

    mouse_click()
    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
left drag | drag:
    # close zoom if open
    tracking.zoom_cancel()

    user.mouse_drag(0)
    # close the mouse grid
    user.grid_close()
# right drag | righty drag:
    # close zoom if open
    tracking.zoom_cancel()

#     user.mouse_drag(1)
#     # close the mouse grid
#     user.grid_close()
# end drag | drag end: user.mouse_drag_end()
