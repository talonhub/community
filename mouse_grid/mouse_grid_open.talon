tag: user.mouse_grid_showing
-
<user.number_key>:
    user.grid_narrow(number_key)
grid off:
    user.grid_close()

grid reset:
    user.grid_reset()

grid back:
    user.grid_go_back()

mouse grid help:
    user.mouse_grid_help_overlay_force_show()
mouse grid help close:
    user.mouse_grid_help_overlay_close()
mouse grid help disable:
    user.mouse_grid_help_overlay_disable()
    user.mouse_grid_help_overlay_close()
mouse grid help enable:
    user.mouse_grid_help_overlay_enable()
    user.mouse_grid_help_overlay_show()
