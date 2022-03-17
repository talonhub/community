from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: mac
app: Chrome
"""

@ctx.action_class('user')
class UserActions:
    def figma_component():actions.key('alt-cmd-k')
    def figma_detach(): actions.key('alt-cmd-b')
    def figma_insert_component(): actions.key('shift-i')

    def figma_group(): actions.key('cmd-g')
    def figma_group_out(): actions.key('shift-cmd-g')
    def figma_frame_that(): actions.key('alt-cmd-g')

    def figma_set_left(): actions.key('alt-a')
    def figma_set_right(): actions.key('alt-d')
    def figma_set_top(): actions.key('alt-w')
    def figma_set_bottom(): actions.key('alt-s')
    def figma_set_horizontal(): actions.key('alt-h')
    def figma_set_vertical(): actions.key('alt-v')

    def figma_text_center(): actions.key('alt-cmd-t')
    def figma_text_left(): actions.key('alt-cmd-l')
    def figma_text_right(): actions.key('alt-cmd-r')

    def figma_tidy_up(): actions.key('ctrl-alt-t')
    def figma_tidy_horizontal(): actions.key('ctrl-alt-h')
    def figma_tidy_vertical(): actions.key('ctrl-alt-v')

    def figma_send_back(): actions.key('[')
    def figma_send_front(): actions.key(']')
    def figma_send_up(): actions.key('cmd-]')
    def figma_send_down(): actions.key('cmd-[')

    def figma_hide(): actions.key('shift-cmd-h')

    def figma_autolayout_add(): actions.key('shift-a')
    def figma_autolayout_remove(): actions.key('alt-shift-a')

    def figma_toggle_ui(): actions.key('cmd-\\')
    def figma_quick_actions(): actions.key('cmd-/')

    def figma_move(): actions.key('v')
    def figma_frame(): actions.key('f')
    def figma_pen(): actions.key('p')
    def figma_pencil(): actions.key('shift-p')
    def figma_text(): actions.key('t')
    def figma_rectangle(): actions.key('r')
    def figma_ellipse(): actions.key('o')
    def figma_line(): actions.key('l')
    def figma_arrow(): actions.key('shift-l')
    def figma_comment(): actions.key('c')
    def figma_pick_color(): actions.key('ctrl-c')
    def figma_slice(): actions.key('s')
    def figma_rulers(): actions.key('shift-r')
    def figma_layout_grids(): actions.key('ctrl-g')
    def figma_layers_panel(): actions.key('alt-1')
    def figma_assets_panel(): actions.key('alt-2')
    def figma_design_panel(): actions.key('alt-8')
    def figma_prototype_panel(): actions.key('alt-9')
    def figma_inspect_panel(): actions.key('alt-0')

    def figma_zoom_in(): actions.key('+')
    def figma_zoom_out(): actions.key('-')
    def figma_zoom_hundred(): actions.key('shift-0')
    def figma_zoom_fit(): actions.key('shift-1')
    def figma_zoom_selection(): actions.key('shift-2')
    def figma_zoom_previous_frame(): actions.key('shift-n')
    def figma_zoom_next_frame(): actions.key('n')
    def figma_previous_page(): actions.key('pageup')
    def figma_next_page(): actions.key('pagedown')
    def figma_find_previous_frame(): actions.key('home')
    def figma_find_next_frame(): actions.key('end')

    def figma_place_image(): actions.key('shift-cmd-k')
    def figma_paste_here(): actions.key('shift-cmd-v')

    def figma_deep_select(): actions.key('ctrl-cmd-t')
    def figma_layer_menu_select(): actions.key('ctrl-cmd-l')

    def figma_rename(): actions.key('cmd-r')

    def figma_style_copy(): actions.key('alt-cmd-c')
    def figma_style_paste(): actions.key('alt-cmd-v')
    def figma_run_plugin(): actions.key('alt-cmd-p')
