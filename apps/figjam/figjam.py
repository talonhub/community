from talon import Module

mod = Module()
mod.apps.figjam = "app.name: Figjam"
mod.apps.figjam = """
tag: browser
win.title: /.*– FigJam/
"""


@mod.action_class
class figjam_actions:
    def figjam_move_tool():
        """Select Move tool"""

    def figjam_sticky_note():
        """Select Sticky note"""

    def figjam_line():
        """Select Line"""

    def figjam_connector():
        """Select Connector"""

    def figjam_marker():
        """Select Marker"""

    def figjam_text_tool():
        """Select Text tool"""

    def figjam_open_assets_panel():
        """Open assets panel"""

    def figjam_place_image():
        """Place image"""

    def figjam_emote_stamp_wheel():
        """Select Emote / Stamp wheel"""

    def figjam_add_show_comments():
        """Add / Show comments"""

    def figjam_show_hide_ui():
        """Show / Hide UI"""

    def figjam_multiplayer_cursors():
        """View Multiplayer cursors"""

    def figjam_pan():
        """Pan view"""

    def figjam_zoom_in():
        """Zoom in"""

    def figjam_zoom_out():
        """Zoom out"""

    def figjam_zoom_to_100_percent():
        """Zoom to 100%"""

    def figjam_zoom_to_fit():
        """Zoom to fit"""

    def figjam_zoom_to_selection():
        """Zoom to selection"""

    def figjam_bold():
        """Apply Bold style to text"""

    def figjam_italic():
        """Apply Italic style to text"""

    def figjam_underline():
        """Apply Underline style to text"""

    def figjam_create_link():
        """Create link in text"""

    def figjam_strikethrough():
        """Apply Strikethrough style to text"""

    def figjam_text_align_left():
        """Align text left"""

    def figjam_text_align_center():
        """Align text center"""

    def figjam_text_align_right():
        """Align text right"""

    def figjam_text_align_justified():
        """Align text justified"""

    def figjam_numbered_list():
        """Create numbered list"""

    def figjam_bulleted_list():
        """Create bulleted list"""

    def figjam_increase_indentation():
        """Increase text indentation"""

    def figjam_decrease_indentation():
        """Decrease text indentation"""

    def figjam_copy():
        """Copy selection"""

    def figjam_cut():
        """Cut selection"""

    def figjam_paste():
        """Paste clipboard content"""

    def figjam_paste_over_selection():
        """Paste over selection"""

    def figjam_bring_forward():
        """Bring object forward"""

    def figjam_send_backward():
        """Send object backward"""

    def figjam_bring_to_front():
        """Bring object to front"""

    def figjam_send_to_back():
        """Send object to back"""

    def figjam_group_selection():
        """Group selected objects"""

    def figjam_lock_unlock_selection():
        """Lock / Unlock selected objects"""

    def figjam_flip_horizontal():
        """Flip object horizontal"""

    def figjam_flip_vertical():
        """Flip object vertical"""

    def figjam_undo():
        """Undo last action"""

    def figjam_redo():
        """Redo last undone action"""

    def figjam_edit_text_while_editing():
        """Edit text while editing"""

    def figjam_align_left():
        """Align objects left"""

    def figjam_align_right():
        """Align objects right"""

    def figjam_align_top():
        """Align objects top"""

    def figjam_align_bottom():
        """Align objects bottom"""

    def figjam_align_center():
        """Align objects center"""

    def figjam_tidy_up():
        """Tidy up objects"""

    def figjam_straight_connector_or_line():
        """Create straight connector or line"""
