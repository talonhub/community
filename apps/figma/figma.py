from talon import Module

mod = Module()
apps = mod.apps
apps.figma = "app.name: Chrome OR app.name: Figma" 


@mod.action_class
class figma_actions:
    def figma_component():
        """Create component"""
    def figma_detach():
        """Detach instance"""
    def figma_insert_component():
        """Insert component and find"""

    def figma_group():
        """Group selection"""
    def figma_group_out():
        """Remove group"""
    def figma_frame_that():
        """Frame selection"""
    def figma_set_left():
        """Align Left"""
    def figma_set_right():
        """Align right"""
    def figma_set_top():
        """Align up"""
    def figma_set_bottom():
        """Align Down"""
    def figma_set_horizontal():
        """Align horizontal"""
    def figma_set_vertical():
        """Align vertical"""

    def figma_text_center():
        """Align text center"""
    def figma_text_left():
        """Align text left"""
    def figma_text_right():
        """Align text right"""

    def figma_tidy_horizontal():
        """Tidy horizontal"""
    def figma_tidy_vertical():
        """Tidy vertical"""
    def figma_tidy_up():
        """Tidy up"""

    def figma_send_back():
        """Send back"""
    def figma_send_front():
        """Send front"""
    def figma_send_up():
        """Send up"""
    def figma_send_down():
        """Send down"""

    def figma_hide():
        """Hide or Show"""

    def figma_autolayout_add():
        """Auto Layout add"""
    def figma_autolayout_remove():
        """Auto Layout remove"""

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

    def figma_place_image():
        """Place image"""
    def figma_paste_here():
        """Paste object here"""


    def figma_deep_select():
        """Deep select"""
    def figma_layer_menu_select():
        """Deep select layer menu"""

    def figma_rename():
        """Rename"""

    def figma_style_copy():
        """Copy the style properties"""
    def figma_style_paste():
        """Paste the style properties"""
    def figma_paste_replace():
        """Paste to replace"""

    def figma_run_plugin():
        """Run the last plugin"""

    def figma_collapse():
        """Collapse layers"""

    def figma_remove():
        """Remove"""

    def figma_paneldesign():
        """Design panel"""

    def figma_panelprototype():
        """Prototype panel"""

    def figma_panelinspect():
        """Inspect panel"""

    # Typography

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