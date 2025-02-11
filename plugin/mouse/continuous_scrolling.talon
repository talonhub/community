tag: user.continuous_scrolling
-
<number_small>: user.mouse_scroll_set_speed(number_small)

[wheel] stop: user.mouse_scroll_stop()
[wheel] stop here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_stop()
