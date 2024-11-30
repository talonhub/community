# window new:                 app.window_open()
# window close:               app.window_close()
# window hide:                app.window_hide()
# window last:                app.window_previous()
# window next:                app.window_next()
# window back:                user.window_focus_last()

# focus {user.running_application}:
#     user.window_focus_name(running_application)

# snap <user.snap_screen>:
#     user.snap_active_window_to_screen(snap_screen)
# snap {user.snap_position}:
#     user.snap_active_window_to_position(snap_position)
# snap <user.snap_screen> {user.snap_position}:
#     user.snap_active_window_to_screen_and_position(snap_screen, snap_position)

# snap this <user.snap_screen>:
#     user.snap_window_under_cursor_to_screen(snap_screen)
# snap this {user.snap_position}:
#     user.snap_window_under_cursor_to_position(snap_position)
# snap this <user.snap_screen> {user.snap_position}:
#     user.snap_window_under_cursor_to_screen_and_position(snap_screen, snap_position)

# snap {user.running_application} <user.snap_screen>:
#     user.snap_application_to_screen(running_application, snap_screen)
# snap {user.running_application} {user.snap_position}:
#     user.snap_application_to_position(running_application, snap_position)
# snap {user.running_application} <user.snap_screen> {user.snap_position}:
#     user.snap_application_to_screen_and_position(running_application, snap_screen, snap_position)

# (snap | move) back:
#     user.revert_active_window_position()
# (snap | move) this back:
#     user.revert_window_under_cursor_position()
# (snap | move) {user.running_application} back:
#     user.revert_application_window_position(running_application)

# snap {user.running_application}:
#     user.swap_active_window_position_with_application(running_application)

# move center:                user.move_window_to_screen_center()
# move here:                  user.move_window_side_to_cursor_position()
# side here:                  user.resize_window_side_to_cursor_position()

# move {user.resize_side} {user.resize_direction} [{user.resize_size}]:
#     user.window_resize(resize_side, resize_direction, resize_size or "medium")

# screen numbers:             user.screens_show_numbering()
