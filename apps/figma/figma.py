from talon import Module

mod = Module()
mod.apps.figma = "app.name: Figma"
mod.apps.figma = """
tag: browser
win.title: /.*– Figma/
"""


@mod.action_class
class figma_actions:
    def figma_toggle_ui():
        """Show/hide sidebars"""

    def figma_quick_actions():
        """Quick actions bar"""

    def figma_move():
        """Move tool"""

    def figma_frame():
        """Frame tool"""

    def figma_pen():
        """Pen tool"""

    def figma_pencil():
        """Pencil tool"""

    def figma_text():
        """Text tool"""

    def figma_rectangle():
        """Rectangle tool"""

    def figma_ellipse():
        """Ellipse tool"""

    def figma_line():
        """Line tool"""

    def figma_arrow():
        """Arrow tool"""

    def figma_comment():
        """Add comment"""

    def figma_pick_color():
        """Pick color"""

    def figma_slice():
        """Slice tool"""

    def figma_rulers():
        """Rulers"""

    def figma_layout_grids():
        """Layout grids"""

    def figma_layers_panel():
        """Open layers panel"""

    def figma_assets_panel():
        """Open assets panel"""

    def figma_design_panel():
        """Open design panel"""

    def figma_prototype_panel():
        """Open prototype panel"""

    def figma_inspect_panel():
        """Open inspect panel"""

    def figma_pan():
        """Pan"""

    def figma_pan_stop():
        """Pan stop"""

    def figma_zoom_in():
        """Zoom in"""

    def figma_zoom_out():
        """Zoom out"""

    def figma_zoom_hundred():
        """Zoom to 100%"""

    def figma_zoom_fit():
        """Zoom to fit"""

    def figma_zoom_selection():
        """Zoom to selection"""

    def figma_zoom_previous_frame():
        """Zoom to previous frame"""

    def figma_zoom_next_frame():
        """Zoom to next frame"""

    def figma_previous_page():
        """Previous page"""

    def figma_next_page():
        """Next page"""

    def figma_find_previous_frame():
        """Find previous frame"""

    def figma_find_next_frame():
        """Fine next frame"""

    def figma_bold():
        """Bold"""

    def figma_underline():
        """Underline"""

    def figma_strikethrough():
        """Strike Through"""

    def figma_transform_list():
        """Turn into a list"""

    def figma_text_align_left():
        """Text align left"""

    def figma_text_align_right():
        """Text align right"""

    def figma_text_align_center():
        """Text align center"""

    def figma_text_align_justified():
        """Text align justified"""

    def figma_adjust_font_size_up():
        """Adjust font size bigger"""

    def figma_adjust_font_size_down():
        """Adjust font size smaller"""

    def figma_adjust_font_weight_up():
        """Adjust font weight bigger"""

    def figma_adjust_font_weight_down():
        """Adjust font weight smaller"""

    def figma_adjust_letter_spacing_up():
        """Adjust letter spacing bigger"""

    def figma_adjust_letter_spacing_down():
        """Adjust letter spacing smaller"""

    def figma_adjust_line_height_up():
        """Adjust line height bigger"""

    def figma_adjust_line_height_down():
        """Adjust line height smaller"""

    def figma_select_all():
        """Select all"""

    def figma_select_inverse():
        """Select inverse"""

    def figma_deep_select():
        """Deep select"""

    def figma_select_layer_menu():
        """Select layer menu"""

    def figma_select_children():
        """Select children"""

    def figma_select_parent():
        """Select parent"""

    def figma_select_next_sibling():
        """Select next sibling"""

    def figma_select_prev_sibling():
        """Select previous sibling"""

    def figma_group_selection():
        """Group selection"""

    def figma_ungroup_selection():
        """Ungroup selection"""

    def figma_frame_selection():
        """Frame selection"""

    def figma_toggle_hide_selection():
        """Show/Hide selection"""

    def figma_toggle_lock_selection():
        """Lock/Unlock selection"""

    def figma_duplicate():
        """Duplicate"""

    def figma_rename_selection():
        """Rename selection"""

    def figma_flip_horizontal():
        """Flip horizontal"""

    def figma_flip_vertical():
        """Flip vertical"""

    def figma_use_as_mask():
        """Use as mask"""

    def figma_bring_forward():
        """Bring forward"""

    def figma_send_backward():
        """Send backward"""

    def figma_bring_to_front():
        """Bring to front"""

    def figma_send_to_back():
        """Send to back"""

    def figma_align_left():
        """Align left"""

    def figma_align_right():
        """Align right"""

    def figma_align_top():
        """Align top"""

    def figma_align_bottom():
        """Align bottom"""

    def figma_align_center_horizontal():
        """Align center horizontal"""

    def figma_align_center_vertical():
        """Align center vertical"""

    def figma_distribute_spacing_horizontal():
        """Distributes spacing horizontal"""

    def figma_distribute_spacing_vertical():
        """Distributes spacing vertical"""

    def figma_tidy_up():
        """Tidy up"""

    def figma_auto_layout():
        """Auto layout"""

    def figma_remove_auto_layout():
        """Remove auto layout"""

    def figma_create_component():
        """Create component"""

    def figma_detach_instance():
        """Detach instance"""

    def figma_insert_component():
        """Insert component"""

    def figma_swap_instance():
        """Swap instance"""
