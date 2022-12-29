tag: user.marker_ui_showing
-
marker hide:
    user.marker_ui_hide()

jump {user.marker_ui_label}:
    user.marker_ui_mouse_move(marker_ui_label)
    user.marker_ui_hide()

touch {user.marker_ui_label}:
    user.marker_ui_mouse_move(marker_ui_label)
    mouse_click(0)
    user.marker_ui_hide()

righty {user.marker_ui_label}:
    user.marker_ui_mouse_move(marker_ui_label)
    mouse_click(1)
    user.marker_ui_hide()

midclick {user.marker_ui_label}:
    user.marker_ui_mouse_move(marker_ui_label)
    mouse_click(2)
    user.marker_ui_hide()

# Versions that don't close the overlay

jump {user.marker_ui_label} more:
    user.marker_ui_mouse_move(marker_ui_label)

touch {user.marker_ui_label} more:
    user.marker_ui_mouse_move(marker_ui_label)
    mouse_click(0)

righty {user.marker_ui_label} more:
    user.marker_ui_mouse_move(marker_ui_label)
    mouse_click(1)

midclick {user.marker_ui_label} more:
    user.marker_ui_mouse_move(marker_ui_label)
    mouse_click(2)
