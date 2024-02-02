from talon import Context, actions, ctrl

ctx = Context()
ctx.matches = r"""
os: windows
app: Figma
"""


@ctx.action_class("user")
class UserActions:
    def figma_toggle_ui():
        actions.key("ctrl-\\")

    def figma_quick_actions():
        actions.key("ctrl-/")

    def figma_move():
        actions.key("v")

    def figma_hand():
        actions.key("h")

    def figma_frame():
        actions.key("f")

    def figma_pen():
        actions.key("p")

    def figma_pencil():
        actions.key("shift-p")

    def figma_text():
        actions.key("t")

    def figma_rectangle():
        actions.key("r")

    def figma_ellipse():
        actions.key("o")

    def figma_line():
        actions.key("l")

    def figma_arrow():
        actions.key("shift-l")

    def figma_comment():
        actions.key("c")

    def figma_pick_color():
        actions.key("i")

    def figma_slice():
        actions.key("s")

    def figma_rulers():
        actions.key("shift-r")

    def figma_layout_grids():
        actions.key("ctrl-shift-4")

    def figma_layers_panel():
        actions.key("alt-1")

    def figma_assets_panel():
        actions.key("alt-2")

    def figma_design_panel():
        actions.key("alt-8")

    def figma_prototype_panel():
        actions.key("alt-9")

    def figma_inspect_panel():
        actions.key("alt-0")

    def figma_pan():
        ctrl.key_press("space", down=True)
        ctrl.mouse_click(button=1, down=True)
        ctrl.key_press("space", up=True)

    def figma_pan_stop():
        ctrl.mouse_click(button=1, up=True)

    def figma_zoom_in():
        actions.key("ctrl-=")

    def figma_zoom_out():
        actions.key("ctrl--")

    def figma_zoom_hundred():
        actions.key("ctrl-0")

    def figma_zoom_fit():
        actions.key("shift-1")

    def figma_zoom_selection():
        actions.key("shift-2")

    def figma_zoom_previous_frame():
        actions.key("shift-n")

    def figma_zoom_next_frame():
        actions.key("n")

    def figma_previous_page():
        actions.key("pageup")

    def figma_next_page():
        actions.key("pagedown")

    def figma_find_previous_frame():
        actions.key("home")

    def figma_find_next_frame():
        actions.key("end")

    def figma_bold():
        actions.key("ctrl-b")

    def figma_underline():
        actions.key("ctrl-u")

    def figma_strikethrough():
        actions.key("shift-ctrl-x")

    def figma_transform_list():
        actions.key("shift-ctrl-7")

    def figma_text_align_left():
        actions.key("alt-ctrl-l")

    def figma_text_align_right():
        actions.key("alt-ctrl-r")

    def figma_text_align_center():
        actions.key("alt-ctrl-t")

    def figma_text_align_justified():
        actions.key("alt-ctrl-j")

    def figma_adjust_font_size_up():
        actions.key("shift-ctrl->")

    def figma_adjust_font_size_down():
        actions.key("shift-ctrl-<")

    def figma_adjust_font_weight_up():
        actions.key("alt-ctrl-.")

    def figma_adjust_font_weight_down():
        actions.key("alt-ctrl-,")

    def figma_adjust_letter_spacing_up():
        actions.key("alt-.")

    def figma_adjust_letter_spacing_down():
        actions.key("alt-,")

    def figma_adjust_line_height_up():
        actions.key("shift-alt->")

    def figma_adjust_line_height_down():
        actions.key("shift-alt-<")

    def figma_select_all():
        actions.key("ctrl-a")

    def figma_select_inverse():
        actions.key("shift-ctrl-a")

    def figma_deep_select():
        ctrl.key_press("ctrl", down=True)
        ctrl.mouse_click(button=0, wait=16000)
        ctrl.key_press("ctrl", up=True)

    def figma_select_layer_menu():
        ctrl.key_press("ctrl", down=True)
        ctrl.mouse_click(button=1, wait=16000)
        ctrl.key_press("ctrl", up=True)

    def figma_select_children():
        actions.key("enter")

    def figma_select_parent():
        actions.key("shift-enter")

    def figma_select_next_sibling():
        actions.key("tab")

    def figma_select_prev_sibling():
        actions.key("shift-tab")

    def figma_group_selection():
        actions.key("ctrl-g")

    def figma_ungroup_selection():
        actions.key("shift-ctrl-g")

    def figma_frame_selection():
        actions.key("ctrl-alt-g")

    def figma_toggle_hide_selection():
        actions.key("ctrl-shift-h")

    def figma_toggle_lock_selection():
        actions.key("ctrl-shift-l")

    def figma_duplicate():
        actions.key("ctrl-d")

    def figma_rename_selection():
        actions.key("ctrl-r")

    def figma_bring_forward():
        actions.key("ctrl-]")

    def figma_send_backward():
        actions.key("ctrl-[")

    def figma_bring_to_front():
        actions.key("]")

    def figma_send_to_back():
        actions.key("[")

    def figma_align_left():
        actions.key("alt-a")

    def figma_align_right():
        actions.key("alt-d")

    def figma_align_top():
        actions.key("alt-w")

    def figma_align_bottom():
        actions.key("alt-s")

    def figma_align_center_horizontal():
        actions.key("alt-h")

    def figma_align_center_vertical():
        actions.key("alt-v")

    def figma_distribute_spacing_horizontal():
        actions.key("alt-shift-h")

    def figma_distribute_spacing_vertical():
        actions.key("alt-shift-v")

    def figma_tidy_up():
        actions.key("ctrl-alt-shift-t")

    def figma_auto_layout():
        actions.key("shift-a")

    def figma_remove_auto_layout():
        actions.key("alt-shift-a")

    def figma_create_component():
        actions.key("ctrl-alt-k")

    def figma_detach_instance():
        actions.key("ctrl-alt-b")

    def figma_insert_component():
        actions.key("shift-i")

    def figma_swap_instance():
        actions.key("alt")
