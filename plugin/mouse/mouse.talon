hissing mode: user.toggle_hiss_click()

(control | see) mouse: tracking.control_toggle()
(control | see) (zoom | mouse): user.mouse_toggle_zoom_mouse()
camera overlay: user.mouse_toggle_camera_overlay()
run calibration: tracking.calibrate()

# New Control Toggles

# control mouse: tracking.control_toggle()
# control off: user.mouse_sleep()
zoom mouse: tracking.control_zoom_toggle()
# camera overlay: tracking.control_debug_toggle()
# run calibration: tracking.calibrate()
# All commands you can call for tracking
# ---------------------------------------------
# tracking.calibrate
# tracking.control1_enabled
# tracking.control1_toggle
# tracking.control_debug_toggle
# tracking.control_enabled
# tracking.control_gaze_toggle
# tracking.control_head_toggle
# tracking.control_mouse_jump_toggle
# tracking.control_toggle
# tracking.control_zoom_enabled
# tracking.control_zoom_toggle
# tracking.zoom
# tracking.zoom_cancel

(control | see) mouse: user.mouse_toggle_control_mouse()
(control | see) (zoom | mouse): tracking.control_zoom_toggle()
camera overlay: tracking.control_debug_toggle()
run calibration: tracking.calibrate()

# New commands / Toggles changed to "tracking"
# ---------------------------------------------
#control mouse: tracking.control1_toggle()
zoom mouse: tracking.control_zoom_toggle()
cancel zoom mouse: tracking.zoom_cancel()
#control mouse: tracking.control_toggle()

# Old Toggles
# user.mouse_calibrate()
# user.mouse_toggle_control_mouse()

touch:
    mouse_click(0)
    # close the mouse grid if open
    user.grid_close()
    # End any open drags
    # Touch automatically ends left drags so this is for right drags specifically
    user.mouse_drag_end()

righty:
    mouse_click(1)
    # close the mouse grid if open
    user.grid_close()

mid click:
    mouse_click(2)
    # close the mouse grid
    user.grid_close()

#see keys.py for modifiers.
#defaults
#command
#control
#option = alt
#shift
#super = windows key
<user.modifiers> touch:
    key("{modifiers}:down")
    mouse_click(0)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
<user.modifiers> righty:
    key("{modifiers}:down")
    mouse_click(1)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
(dub click | duke):
    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
(trip click | trip lick):
    mouse_click()
    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
left drag | drag:
    user.mouse_drag(0)
    # close the mouse grid
    user.grid_close()
right drag | righty drag:
    user.mouse_drag(1)
    # close the mouse grid
    user.grid_close()
end drag | drag end: user.mouse_drag_end()
wheel down: user.mouse_scroll_down()
wheel down here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down()
wheel tiny [down]: user.mouse_scroll_down(0.2)
wheel tiny [down] here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down(0.2)
wheel downer: user.mouse_scroll_down_continuous()
wheel downer here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down_continuous()
wheel up: user.mouse_scroll_up()
wheel up here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up()
wheel tiny up: user.mouse_scroll_up(0.2)
wheel tiny up here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up(0.2)
wheel upper: user.mouse_scroll_up_continuous()
wheel upper here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up_continuous()
(wheel gaze | gaze | scrolls): user.mouse_gaze_scroll()
wheel gaze here:
    user.mouse_move_center_active_window()
    user.mouse_gaze_scroll()
wheel stop: user.mouse_scroll_stop()
wheel stop here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_stop()
wheel left: user.mouse_scroll_left()
wheel left here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_left()
wheel tiny left: user.mouse_scroll_left(0.5)
wheel tiny left here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_left(0.5)
wheel right: user.mouse_scroll_right()
wheel right here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_right()
wheel tiny right: user.mouse_scroll_right(0.5)
wheel tiny right here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_right(0.5)
copy mouse position: user.copy_mouse_position()
curse no:
    # Command added 2021-12-13, can remove after 2022-06-01
    app.notify("Please activate the user.mouse_cursor_commands_enable tag to enable this command")
