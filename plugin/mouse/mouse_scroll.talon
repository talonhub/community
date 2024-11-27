# wheel down: user.mouse_scroll_down()
# wheel down here:
#     user.mouse_move_center_active_window()
#     user.mouse_scroll_down()
# wheel tiny [down]: user.mouse_scroll_down(0.2)
# wheel tiny [down] here:
#     user.mouse_move_center_active_window()
#     user.mouse_scroll_down(0.2)
wheel fall [<number_small>]: 
    numb = number_small or 1
    user.mouse_scroll_down_continuous()
    repeat(numb - 1)

# wheel downer here:
#     user.mouse_move_center_active_window()
#     user.mouse_scroll_down_continuous()
# wheel up: user.mouse_scroll_up()
# wheel up here:
#     user.mouse_move_center_active_window()
#     user.mouse_scroll_up()
# wheel tiny up: user.mouse_scroll_up(0.2)
# wheel tiny up here:
#     user.mouse_move_center_active_window()
#     user.mouse_scroll_up(0.2)
wheel (rise) [<number_small>]: 
    numb = number_small or 1
    user.mouse_scroll_up_continuous()
    repeat(numb - 1)
