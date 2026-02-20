control mouse: tracking.control_toggle()
control off: user.mouse_sleep()
zoom mouse: tracking.control_zoom_toggle()
camera overlay: tracking.control_debug_toggle()
run calibration: tracking.calibrate()

(touch | cricket):
    # close zoom if open
    user.zoom_close()
    mouse_click(0)
    # close the mouse grid if open
    user.grid_close()
    # End any open drags
    # Touch automatically ends left drags so this is for right drags specifically
    user.mouse_drag_end()

(righty | psychic):
    # close zoom if open
    user.zoom_close()
    mouse_click(1)
    # close the mouse grid if open
    user.grid_close()

mid click:
    # close zoom if open
    user.zoom_close()
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
    # close zoom if open
    user.zoom_close()
    key("{modifiers}:down")
    mouse_click(0)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
<user.modifiers> (righty | psychic):
    # close zoom if open
    user.zoom_close()
    key("{modifiers}:down")
    mouse_click(1)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
(dub click | duke):
    # close zoom if open
    user.zoom_close()
    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
(trip click | trip lick):
    # close zoom if open
    user.zoom_close()
    mouse_click()
    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
left drag | drag | drag start:
    # close zoom if open
    user.zoom_close()
    user.mouse_drag(0)
    # close the mouse grid
    user.grid_close()
right drag | righty drag:
    # close zoom if open
    user.zoom_close()
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
(wheel gaze | scrolly): user.mouse_gaze_scroll()
wheel gaze here:
    user.mouse_move_center_active_window()
    user.mouse_gaze_scroll()
(well stop | scroll stop | wheel stop): user.mouse_scroll_stop()

downer: user.mouse_scroll_down()
downer tiny: mouse_scroll(20)
upper: user.mouse_scroll_up()
upper tiny: mouse_scroll(-20)
track left: mouse_scroll(0, -80)
page left: mouse_scroll(0, -1600)
track left tiny: mouse_scroll(0, -40)
track right: mouse_scroll(0, 80)
page right: mouse_scroll(0, 1600)
track right tiny: mouse_scroll(0, 40)

curse yes: user.mouse_show_cursor()
curse no: user.mouse_hide_cursor()
curse no:
    # Command added 2021-12-13, can remove after 2022-06-01
    app.notify("Please activate the user.mouse_cursor_commands_enable tag to enable this command")
copy mouse position: user.copy_mouse_position()

#right drag | righty drag:
#	user.mouse_drag(1)
	# close the mouse grid
#	user.grid_close()
#end drag | drag end:
#    user.mouse_drag_end()

#wheel down here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_down()

#wheel downer here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_down_continuous()

#wheel up here:
# 	 user.mouse_scroll_up()

#wheel tiny up here:
#    user.mouse_move_center_active_window()
#    mouse_scroll(-20)

#wheel upper here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_up_continuous()

wheel gaze: user.mouse_gaze_scroll()

#wheel gaze here:
#    user.mouse_move_center_active_window()
#    user.mouse_gaze_scroll()

#wheel stop here:
#    user.mouse_move_center_active_window()
#    user.mouse_scroll_stop()

#wheel left here:
#   user.mouse_move_center_active_window()
#   mouse_scroll(0, -40)

#wheel tiny left here:
#   user.mouse_move_center_active_window()
#   mouse_scroll(0, -20)

#wheel right here:
#    user.mouse_move_center_active_window()
#    mouse_scroll(0, 40)

#wheel tiny right here:
#    user.mouse_move_center_active_window()
#    mouse_scroll(0, 20)

# To scroll with a hiss sound, set mouse_enable_hiss_scroll to true in settings.talon
mouse hiss up: user.hiss_scroll_up()
mouse hiss down: user.hiss_scroll_down()
