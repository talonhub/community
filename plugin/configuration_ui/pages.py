from .setting_file_paths import MODE_INDICATOR_PATH, SUBTITLES_PATH
from .setting_uis import (
    create_boolean_setting,
    create_color_picker_setting,
    create_discrete_choices_setting,
    create_numeric_setting,
    create_tag_setting,
    create_text_setting,
)


class Page:
    def __init__(self, title, description, settings, prefix="", path=None):
        self.title = title
        self.description = description
        self.settings = settings
        self.prefix = prefix
        if path is not None:
            for setting in self.settings:
                setting.path = path


def create_pages():
    return [
        Page(
            "Text Insertion",
            "",
            [
                create_tag_setting("user.unprefixed_numbers"),
                create_numeric_setting("user.paste_to_insert_threshold", -1),
                create_boolean_setting("user.context_sensitive_dictation"),
                create_numeric_setting("user.insert_between_wait", 0),
            ],
        ),
        Page(
            "Speech Recognition",
            "",
            [
                create_numeric_setting("speech.timeout", 0.0),
                create_discrete_choices_setting(
                    "user.initial_mode",
                    [
                        (mode, f"{mode} mode")
                        for mode in ("dictation", "command", "mixed", "sleep")
                    ],
                ),
                create_numeric_setting("user.listening_timeout_minutes", -1),
            ],
        ),
        Page(
            "Scrolling",
            "",
            [
                create_numeric_setting("user.mouse_continuous_scroll_amount", 0.0),
                create_numeric_setting("user.mouse_gaze_scroll_speed_multiplier", 0.0),
                create_numeric_setting("user.mouse_continuous_scroll_acceleration", 1.0),
                create_boolean_setting("user.mouse_enable_pop_stops_scroll"),
                create_boolean_setting("user.mouse_enable_hiss_scroll"),
                create_numeric_setting("user.hiss_scroll_debounce_time", 0),
                create_boolean_setting("user.mouse_hide_mouse_gui"),
                create_numeric_setting("user.mouse_wheel_down_amount", 0),
                create_numeric_setting("user.mouse_wheel_horizontal_amount", 0),
            ],
        ),
        Page(
            "Mouse Grid",
            "",
            [
                create_boolean_setting("user.grids_put_one_bottom_left"),
                create_boolean_setting("user.grid_show_zoomed"),
            ],
        ),
        Page(
            "Command History",
            "",
            [
                create_numeric_setting("user.command_history_display", 1),
                create_numeric_setting("user.command_history_size", 1),
            ],
        ),
        Page(
            "Popping",
            "Decide what should happen when you make a popping noise",
            [
                create_tag_setting("user.pop_twice_to_repeat"),
                create_tag_setting("user.pop_twice_to_wake"),
                create_numeric_setting("user.double_pop_speed_minimum", 0.0),
                create_numeric_setting("user.double_pop_speed_maximum", 0.0),
                create_discrete_choices_setting(
                    "user.mouse_enable_pop_click",
                    [
                        (0, "off"),
                        (1, "on with eyetracker but not zoom mouse mode"),
                        (2, "on but not with zoom mouse mode"),
                    ],
                    is_numeric=True,
                ),
                create_boolean_setting("user.mouse_enable_pop_stops_scroll"),
                create_boolean_setting("user.mouse_enable_pop_stops_drag"),
            ],
        ),
        Page(
            "Help System",
            "",
            [
                create_numeric_setting("user.help_max_command_lines_per_page", 1),
                create_numeric_setting("user.help_max_contexts_per_page", 1),
                create_boolean_setting("user.help_sort_contexts_by_specificity"),
            ],
        ),
        Page(
            "Window Management",
            "",
            [
                create_discrete_choices_setting(
                    "user.window_snap_screen",
                    [(option, option) for option in ("proportional", "size aware")],
                ),
                create_tag_setting("user.experimental_window_layout"),
            ],
        ),
        Page(
            "Mode Indicator",
            "The mode indicator shows a colored circle indicating which mode is active.",
            [
                create_boolean_setting(
                    "user.mode_indicator_show",
                ),
                create_boolean_setting("user.mode_indicator_show_microphone_name"),
                create_numeric_setting("user.mode_indicator_size", 1),
                create_numeric_setting(
                    "user.mode_indicator_x",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                create_numeric_setting(
                    "user.mode_indicator_y",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                create_numeric_setting(
                    "user.mode_indicator_color_alpha",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                create_numeric_setting(
                    "user.mode_indicator_color_gradient",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                create_color_picker_setting("user.mode_indicator_color_text"),
                create_color_picker_setting("user.mode_indicator_color_mute"),
                create_color_picker_setting("user.mode_indicator_color_sleep"),
                create_color_picker_setting("user.mode_indicator_color_deep_sleep"),
                create_color_picker_setting("user.mode_indicator_color_dictation"),
                create_color_picker_setting("user.mode_indicator_color_mixed"),
                create_color_picker_setting("user.mode_indicator_color_command"),
                create_color_picker_setting("user.mode_indicator_color_other"),
            ],
            prefix="user.mode_indicator_",
            path=MODE_INDICATOR_PATH,
        ),
        Page(
            "Subtitles",
            "Configuration for Community's subtitles (not the Talon builtin subtitles)",
            [
                create_boolean_setting("user.subtitles_show"),
                create_discrete_choices_setting(
                    "user.subtitles_screens",
                    choices=[
                        ("all", "all screens"),
                        ("main", "main screen as configured in OS"),
                        ("cursor", "screen containing mouse pointer"),
                        ("focus", "screen containing active/focused window/app"),
                    ],
                ),
                create_numeric_setting("user.subtitles_size", 0),
                create_color_picker_setting("user.subtitles_color"),
                create_color_picker_setting("user.subtitles_color_outline"),
                create_numeric_setting("user.subtitles_timeout_per_char", 0),
                create_numeric_setting("user.subtitles_timeout_min", 0),
                create_numeric_setting("user.subtitles_timeout_max", 0),
                create_numeric_setting(
                    "user.subtitles_y",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
            ],
            prefix="user.subtitles_",
            path=SUBTITLES_PATH,
        ),
        Page(
            "Snippets",
            "",
            [
                create_numeric_setting("user.snippet_raw_text_spaces_per_tab", -1),
                create_text_setting("user.snippets_dir"),
            ],
        ),
        Page(
            "Miscellaneous",
            "",
            [
                create_numeric_setting("user.mouse_click_hold", 0),
                create_boolean_setting("user.file_manager_auto_show_pickers"),
                create_boolean_setting("user.strict_command_deprecation"),
                create_numeric_setting("user.selected_text_timeout", 0.0),
                create_tag_setting("user.mouse_cursor_commands_enable"),
            ],
        ),
    ]
