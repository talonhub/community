user.operating_system: windows 10
app: windows_explorer
app: windows_file_browser
-
tag(): user.file_manager
tag(): user.tabs


slice take:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2024-01-15_18.53.04.935105.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()


copy take:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2024-01-15_18.54.41.449635.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

delete take:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2024-01-15_18.56.27.314708.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

rename that:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2024-01-15_18.55.33.505920.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()
