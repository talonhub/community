from talon import Context, actions, ctrl

ctx = Context()
ctx.matches = r"""
os: windows
app: Figjam
"""


@ctx.action_class("user")
class UserActions:
    def figjam_move_tool():
        actions.key("v")

    def figjam_sticky_note():
        actions.key("s")

    def figjam_line():
        actions.key("l")

    def figjam_connector():
        actions.key("shift-c")

    def figjam_marker():
        actions.key("m")

    def figjam_text_tool():
        actions.key("t")

    def figjam_open_assets_panel():
        actions.key("alt-2")

    def figjam_place_image():
        actions.key("shift-ctrl-k")

    def figjam_emote_stamp_wheel():
        actions.key("e")

    def figjam_add_show_comments():
        actions.key("c")

    def figjam_show_hide_ui():
        actions.key("ctrl-\\")

    def figjam_multiplayer_cursors():
        actions.key("alt-ctrl-\\")

    def figjam_pan():
        actions.key("space-drag")

    def figjam_zoom_in():
        actions.key("+")

    def figjam_zoom_out():
        actions.key("-")

    def figjam_zoom_to_100_percent():
        actions.key("shift-0")

    def figjam_zoom_to_fit():
        actions.key("shift-1")

    def figjam_zoom_to_selection():
        actions.key("shift-2")

    def figjam_bold():
        actions.key("ctrl-b")

    def figjam_italic():
        actions.key("ctrl-i")

    def figjam_underline():
        actions.key("ctrl-u")

    def figjam_create_link():
        actions.key("ctrl-k")

    def figjam_strikethrough():
        actions.key("shift-ctrl-x")

    def figjam_text_align_left():
        actions.key("alt-ctrl-l")

    def figjam_text_align_center():
        actions.key("alt-ctrl-t")

    def figjam_text_align_right():
        actions.key("alt-ctrl-r")

    def figjam_text_align_justified():
        actions.key("alt-ctrl-j")

    def figjam_numbered_list():
        actions.key("shift-ctrl-7")

    def figjam_bulleted_list():
        actions.key("shift-ctrl-8")

    def figjam_increase_indentation():
        actions.key("ctrl-]")

    def figjam_decrease_indentation():
        actions.key("ctrl-[")

    def figjam_copy():
        actions.key("ctrl-c")

    def figjam_cut():
        actions.key("ctrl-x")

    def figjam_paste():
        actions.key("ctrl-v")

    def figjam_paste_over_selection():
        actions.key("shift-ctrl-v")

    def figjam_bring_forward():
        actions.key("ctrl-]")

    def figjam_send_backward():
        actions.key("ctrl-[")

    def figjam_bring_to_front():
        actions.key("alt-ctrl-]")

    def figjam_send_to_back():
        actions.key("alt-ctrl-[")

    def figjam_group_selection():
        actions.key("ctrl-g")

    def figjam_lock_unlock_selection():
        actions.key("shift-ctrl-l")

    def figjam_flip_horizontal():
        actions.key("shift-h")

    def figjam_flip_vertical():
        actions.key("shift-v")

    def figjam_undo():
        actions.key("ctrl-z")

    def figjam_redo():
        actions.key("shift-ctrl-z")

    def figjam_new_shape_sticky_while_editing():
        actions.key("ctrl-return")

    def figjam_align_left():
        actions.key("alt-a")

    def figjam_align_right():
        actions.key("alt-d")

    def figjam_align_top():
        actions.key("alt-w")

    def figjam_align_bottom():
        actions.key("alt-s")

    def figjam_align_center():
        actions.key("alt-h alt-v")

    def figjam_tidy_up():
        actions.key("ctrl-alt-t")

    def figjam_straight_connector_or_line():
        actions.key("shift-drag")
