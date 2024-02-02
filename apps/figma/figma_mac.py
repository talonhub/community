from talon import Context, actions, ctrl

ctx = Context()
ctx.matches = r"""
os: mac
app: Figma
"""


@ctx.action_class("user")
class UserActions:
    def figma_toggle_ui():
        actions.key("cmd-\\")

    def figma_quick_actions():
        actions.key("cmd-/")

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
        actions.key("ctrl-c")

    def figma_slice():
        actions.key("s")

    def figma_rulers():
        actions.key("shift-r")

    def figma_layout_grids():
        actions.key("ctrl-g")

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

    def figma_zoom_in():
        actions.key("+")

    def figma_zoom_out():
        actions.key("-")

    def figma_zoom_hundred():
        actions.key("shift-0")

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
        actions.key("cmd-b")

    def figma_underline():
        actions.key("cmd-u")

    def figma_strikethrough():
        actions.key("shift-cmd-x")

    def figma_transform_list():
        actions.key("shift-cmd-7")

    def figma_text_align_left():
        actions.key("alt-cmd-l")

    def figma_text_align_right():
        actions.key("alt-cmd-r")

    def figma_text_align_center():
        actions.key("alt-cmd-t")

    def figma_text_align_justified():
        actions.key("alt-cmd-j")

    def figma_adjust_font_size_up():
        actions.key("shift-cmd->")

    def figma_adjust_font_size_down():
        actions.key("shift-cmd-<")

    def figma_adjust_font_weight_up():
        actions.key("alt-cmd-.")

    def figma_adjust_font_weight_down():
        actions.key("alt-cmd-,")

    def figma_adjust_letter_spacing_up():
        actions.key("alt-.")

    def figma_adjust_letter_spacing_down():
        actions.key("alt-,")

    def figma_adjust_line_height_up():
        actions.key("shift-alt->")

    def figma_adjust_line_height_down():
        actions.key("shift-alt-<")

    def figma_select_all():
        actions.key("cmd-a")

    def figma_select_inverse():
        actions.key("shift-cmd-a")

    def figma_deep_select():
        actions.key("")

    def figma_select_layer_menu():
        actions.key("")

    def figma_select_children():
        actions.key("")

    def figma_select_parent():
        actions.key("")

    def figma_select_next_sibling():
        actions.key("")

    def figma_select_prev_sibling():
        actions.key("")

    def figma_group_selection():
        actions.key("")

    def figma_ungroup_selection():
        actions.key("")

    def figma_frame_selection():
        actions.key("")

    def figma_toggle_hide_selection():
        actions.key("")

    def figma_toggle_lock_selection():
        actions.key("")

    def figma_duplicate():
        actions.key("")

    def figma_rename_selection():
        actions.key("")

    # def figma_flip_horizontal(): actions.key('')
    # def figma_flip_vertical(): actions.key('')
    # def figma_use_as_mask(): actions.key('')
    # def figma_bring_forward(): actions.key('')
    # def figma_send_backward(): actions.key('')
    # def figma_bring_to_front(): actions.key('')
    # def figma_send_to_back(): actions.key('')
    # def figma_align_left(): actions.key('')
    # def figma_align_right(): actions.key('')
    # def figma_align_top(): actions.key('')
    # def figma_align_bottom(): actions.key('')
    # def figma_align_center_horizontal(): actions.key('')
    # def figma_align_center_vertical(): actions.key('')
    # def figma_distribute_spacing(): actions.key('')
    # def figma_tidy_up(): actions.key('')
    # def figma_auto_layout(): actions.key('')
    # def figma_remove_auto_layout(): actions.key('')
    # def figma_create_component(): actions.key('')
    # def figma_detach_instance(): actions.key('')
    # def figma_insert_component(): actions.key('')
    # def figma_swap_instance (): actions.key('')
