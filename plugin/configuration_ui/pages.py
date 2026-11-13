from .setting_file_paths import MODE_INDICATOR_PATH, SUBTITLES_PATH
from .setting_uis import (
    Setting,
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
                Setting.tag("user.unprefixed_numbers"),
                Setting.numeric("user.paste_to_insert_threshold", -1),
                Setting.boolean("user.context_sensitive_dictation"),
                Setting.numeric("user.insert_between_wait", 0.0),
            ],
        ),
        Page(
            "Speech Recognition",
            "",
            [
                Setting.numeric("speech.timeout", 0.0),
                Setting.discrete_choices(
                    "user.initial_mode",
                    [
                        (mode, f"{mode} mode")
                        for mode in ("dictation", "command", "mixed", "sleep")
                    ],
                ),
                Setting.numeric("user.listening_timeout_minutes", -1),
            ],
        ),
        Page(
            "Scrolling",
            "",
            [
                Setting.numeric("user.mouse_continuous_scroll_amount", 0),
                Setting.numeric("user.mouse_gaze_scroll_speed_multiplier", 0.0),
                Setting.numeric("user.mouse_continuous_scroll_acceleration", 1.0),
                Setting.boolean("user.mouse_enable_pop_stops_scroll"),
                Setting.boolean("user.mouse_enable_hiss_scroll"),
                Setting.numeric("user.hiss_scroll_debounce_time", 0),
                Setting.boolean("user.mouse_hide_mouse_gui"),
                Setting.numeric("user.mouse_wheel_down_amount", 0),
                Setting.numeric("user.mouse_wheel_horizontal_amount", 0),
            ],
        ),
        Page(
            "Mouse Grid",
            "",
            [
                Setting.boolean("user.grids_put_one_bottom_left"),
                Setting.boolean("user.grid_show_zoomed"),
            ],
        ),
        Page(
            "Command History",
            "",
            [
                Setting.numeric("user.command_history_display", 1),
                Setting.numeric("user.command_history_size", 1),
            ],
        ),
        Page(
            "Popping",
            "Decide what should happen when you make a popping noise",
            [
                Setting.tag("user.pop_twice_to_repeat"),
                Setting.tag("user.pop_twice_to_wake"),
                Setting.numeric("user.double_pop_speed_minimum", 0.0),
                Setting.numeric("user.double_pop_speed_maximum", 0.0),
                Setting.discrete_choices(
                    "user.mouse_enable_pop_click",
                    [
                        (0, "off"),
                        (1, "on with eyetracker but not zoom mouse mode"),
                        (2, "on but not with zoom mouse mode"),
                    ],
                    is_numeric=True,
                ),
                Setting.boolean("user.mouse_enable_pop_stops_scroll"),
                Setting.boolean("user.mouse_enable_pop_stops_drag"),
            ],
        ),
        Page(
            "Help System",
            "",
            [
                Setting.numeric("user.help_max_command_lines_per_page", 1),
                Setting.numeric("user.help_max_contexts_per_page", 1),
                Setting.boolean("user.help_sort_contexts_by_specificity"),
            ],
        ),
        Page(
            "Window Management",
            "",
            [
                Setting.discrete_choices(
                    "user.window_snap_screen",
                    [(option, option) for option in ("proportional", "size aware")],
                ),
                Setting.tag("user.experimental_window_layout"),
            ],
        ),
        Page(
            "Mode Indicator",
            "The mode indicator shows a colored circle indicating which mode is active.",
            [
                Setting.boolean(
                    "user.mode_indicator_show",
                ),
                Setting.boolean("user.mode_indicator_show_microphone_name"),
                Setting.numeric("user.mode_indicator_size", 1),
                Setting.numeric(
                    "user.mode_indicator_x",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                Setting.numeric(
                    "user.mode_indicator_y",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                Setting.numeric(
                    "user.mode_indicator_color_alpha",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                Setting.numeric(
                    "user.mode_indicator_color_gradient",
                    0.0,
                    1.0,
                    use_slider=True,
                ),
                Setting.color("user.mode_indicator_color_text"),
                Setting.color("user.mode_indicator_color_mute"),
                Setting.color("user.mode_indicator_color_sleep"),
                Setting.color("user.mode_indicator_color_deep_sleep"),
                Setting.color("user.mode_indicator_color_dictation"),
                Setting.color("user.mode_indicator_color_mixed"),
                Setting.color("user.mode_indicator_color_command"),
                Setting.color("user.mode_indicator_color_other"),
            ],
            prefix="user.mode_indicator_",
            path=MODE_INDICATOR_PATH,
        ),
        Page(
            "Subtitles",
            "Configuration for Community's subtitles (not the Talon builtin subtitles)",
            [
                Setting.boolean("user.subtitles_show"),
                Setting.discrete_choices(
                    "user.subtitles_screens",
                    choices=[
                        ("all", "all screens"),
                        ("main", "main screen as configured in OS"),
                        ("cursor", "screen containing mouse pointer"),
                        ("focus", "screen containing active/focused window/app"),
                    ],
                ),
                Setting.numeric("user.subtitles_size", 0),
                Setting.color("user.subtitles_color"),
                Setting.color("user.subtitles_color_outline"),
                Setting.numeric("user.subtitles_timeout_per_char", 0),
                Setting.numeric("user.subtitles_timeout_min", 0),
                Setting.numeric("user.subtitles_timeout_max", 0),
                Setting.numeric(
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
                Setting.numeric("user.snippet_raw_text_spaces_per_tab", -1),
                Setting.text("user.snippets_dir"),
            ],
        ),
        Page(
            "Miscellaneous",
            "",
            [
                Setting.numeric("user.mouse_click_hold", 0),
                Setting.boolean("user.file_manager_auto_show_pickers"),
                Setting.boolean("user.strict_command_deprecation"),
                Setting.numeric("user.selected_text_timeout", 0.0),
                Setting.tag("user.mouse_cursor_commands_enable"),
            ],
        ),
    ]
