from pathlib import Path

import egui
from talon import Context, Module, clip, fs, registry

from ...core.gui.gui import let_user_use_page_keys_to_scroll_scroll_area, open_gui
from .setting_file_paths import MODE_INDICATOR_PATH, RELEVANT_PATHS, SUBTITLES_PATH
from .setting_uis import (
    Setting,
    create_boolean_setting,
    create_color_picker_setting,
    create_discrete_choices_setting,
    create_numeric_setting,
    create_tag_setting,
    create_text_setting,
)
from .talon_file_parsing import (
    VALUE_UNAVAILABLE,
    SettingFileSettingInformation,
    parse_settings,
)
from .talon_file_output import update_setting

mod = Module()
ctx = Context()

mod.tag(
    "community_settings_window",
    desc="Community settings configuration window is open. (When possible, this tag will be limited to when the window is focused)",
)
mod.list(
    "community_settings_window_page",
    desc="The name of a page in the Community settings window",
)
mod.list(
    "community_settings_window_setting",
    desc="The name of a setting on the current Community settings window page",
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


def _update_setting_information(
    setting: Setting, file_setting_information: SettingFileSettingInformation
):
    setting.value = egui.Mutable(file_setting_information.value)
    setting.is_activated = file_setting_information.is_activated
    if setting.first_value == VALUE_UNAVAILABLE:
        setting.first_value = file_setting_information.value
    if not setting.is_tag and setting.default_value == VALUE_UNAVAILABLE:
        declaration = registry.decls.settings[setting.name]
        default = declaration.default
        if isinstance(default, declaration.type):
            setting.default_value = default


def _update_setting_information_based_on_file_update(setting: Setting, tags, settings):
    """Update the setting information in response to its containing file updating. tags and settings are from the parsed file"""
    name = setting.name
    source = tags if setting.is_tag else settings
    if name in source:
        updated_information = source[name]
        _update_setting_information(setting, updated_information)
    else:
        setting.value.set(VALUE_UNAVAILABLE)


def compute_readable_name(setting_name, page_prefix: str):
    words = []
    if page_prefix and page_prefix in setting_name:
        name = setting_name[len(page_prefix) :]
    else:
        prefix, name = setting_name.split(".")
        if prefix != "user":
            words.append(prefix)
    words.extend(name.split("_"))
    capitalized_words = [w.capitalize() for w in words]
    return " ".join(capitalized_words)


MAIN_PAGE_NAME = "Main"


class Manager:
    def __init__(self):
        pages = [
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
                    create_numeric_setting("user.mouse_continuous_scroll_amount", 1),
                    create_numeric_setting(
                        "user.mouse_gaze_scroll_speed_multiplier", 1.0
                    ),
                    create_numeric_setting(
                        "user.mouse_continuous_scroll_acceleration", 1
                    ),
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
        self.pages = {page.title: page for page in pages}
        self.page = MAIN_PAGE_NAME
        for path in RELEVANT_PATHS:
            self.on_file_change(path)
        self.error_message = ""
        self.error_setting = None
        ctx.lists["user.community_settings_window_page"] = {
            page.title: page.title for page in pages
        }
        self.chosen_setting = ""
        self.comment_toggle_setting = ""
        self.post_action = None

    def update_page(self, page_name):
        self.page = page_name
        if self.page == MAIN_PAGE_NAME:
            ctx.lists["user.community_settings_window_setting"] = {}
            return
        page = self.pages[self.page]
        ctx.lists["user.community_settings_window_setting"] = {
            compute_readable_name(setting.name, page.prefix): setting.name
            for setting in page.settings
        }

    def _get_settings_at_path(self, path):
        return (
            setting
            for page in self.pages.values()
            for setting in page.settings
            if setting.path == path
        )

    def on_file_change(self, path):
        """Update setting values rendered in response to the .talon file at path changing'"""
        tags, settings = parse_settings(path)
        for setting in self._get_settings_at_path(path):
            _update_setting_information_based_on_file_update(setting, tags, settings)

    async def render_settings_configuration_gui(self, ui, ui_wrapper):
        # set these at the start to avoid a situation where these are set in the middle of this function leading to an invalid state
        post_action = self.post_action
        chosen_setting = self.chosen_setting
        comment_toggle_setting = self.comment_toggle_setting
        old_error_message = self.error_message

        total_available_height = ui.available_height()
        async with ui.horizontal():
            await self._render_page_navigation(ui, total_available_height)

            # put the page on the space to the right of the page navigation
            available_width = ui.available_width()
            interaction_region_space = egui.Vec2(
                available_width, total_available_height
            )

            async with (
                ui.allocate_ui(interaction_region_space) as interaction_ui,
                ui.vertical(),
            ):
                await self._render_current_page(
                    interaction_ui,
                    ui_wrapper,
                    total_available_height,
                    chosen_setting,
                    comment_toggle_setting,
                )

        # cleanup state and handle post action
        if chosen_setting:
            self.chosen_setting = ""
            settings_gui.refresh()
        if comment_toggle_setting:
            self.comment_toggle_setting = ""
            settings_gui.refresh()
        if post_action:
            post_action()
            settings_gui.refresh()
            self.post_action = None
        if old_error_message != self.error_message:
            settings_gui.refresh()

    async def _render_page_navigation(self, ui, total_available_height):
        async with ui.vertical():
            for page in self.pages:
                if ui.selectable_label(page == self.page, f"Page {page}").clicked():
                    self.update_page(page)
            ui.add_space(total_available_height - ui.min_size().y)
        ui.separator()

    async def _render_current_page(
        self,
        ui,
        ui_wrapper,
        total_available_height,
        chosen_setting,
        comment_toggle_setting,
    ):
        if self.page == MAIN_PAGE_NAME:
            await self._render_main_page(ui, total_available_height)
            return

        if self.error_message:
            await self._render_error_message(
                ui, ui_wrapper, self.error_message, self.error_setting
            )
        ui.add_space(10)
        await self._render_configuration_page(
            ui,
            ui_wrapper,
            total_available_height,
            chosen_setting,
            comment_toggle_setting,
        )

    async def _render_configuration_page(
        self,
        ui,
        ui_wrapper,
        total_available_height,
        chosen_setting,
        comment_toggle_setting,
    ):
        page = self.pages[self.page]

        async with (
            egui.ScrollArea.vertical()
            .max_height(total_available_height)
            .show() as scroll_ui
        ):
            await let_user_use_page_keys_to_scroll_scroll_area(scroll_ui)

            ui.strong(page.title)
            if page.description:
                ui.label(page.description)
            ui.add_space(5)
            ui.label("* toggle setting that setting in a Community .talon file")
            ui.separator()
            for setting in page.settings:
                is_setting_chosen = setting.name == chosen_setting
                await self._render_setting_row(
                    ui,
                    ui_wrapper,
                    setting,
                    page,
                    is_setting_chosen,
                    comment_toggle_setting,
                )
                ui.separator()
                if is_setting_chosen:
                    self.post_action = setting.post_chosen_action

    async def _render_setting_row(
        self, ui, ui_wrapper, setting, page, is_setting_chosen, comment_toggle_setting
    ):
        """Render the row for a setting"""
        readable_name = compute_readable_name(setting.name, page.prefix)
        error_representation_of_name = f"{readable_name} ({setting.name})"
        async with ui.horizontal():
            await self._render_toggle_commenting_setting_column(
                ui,
                ui_wrapper,
                setting,
                comment_toggle_setting,
                error_representation_of_name,
            )
            async with ui.with_layout(egui.Layout.right_to_left(egui.Align.TOP)):
                async with ui.vertical():
                    ui.strong(readable_name)
                    ui.weak(setting.name)
                    ui.add_space(5)
                    if not setting.renders_description:
                        ui.label(setting.get_description())
                    if setting.value.get() == VALUE_UNAVAILABLE:
                        type_used = "tag" if setting.is_tag else "setting"
                        error_message = f"Something went wrong. The {type_used} {error_representation_of_name} could not be found or could not be parsed."
                        await self._render_error_message(
                            ui, ui_wrapper, error_message, setting
                        )
                    else:
                        await self._render_settings_ui(
                            ui,
                            ui_wrapper,
                            setting,
                            is_setting_chosen,
                            error_representation_of_name,
                        )
                ui.separator()

    async def _render_setting_revert_button(
        self, ui, ui_wrapper, setting, button_text, revert_value
    ):
        async with ui.group(), ui.horizontal_wrapped():
            if ui_wrapper.button(button_text):
                setting.update_function(setting, setting.first_value)
            ui.label(str(revert_value))

    async def _render_settings_ui(
        self, ui, ui_wrapper, setting, is_setting_chosen, error_representation_of_name
    ):
        """Render the ui for changing the setting"""
        old_value = setting.value.get()
        try:
            async with ui.add_enabled_ui(setting.is_activated or setting.is_tag):
                await setting.render(setting, ui, is_setting_chosen)
                value = setting.value.get()
                if old_value != value:
                    setting.update_function(setting, value)
                if setting.first_value != setting.value.get():
                    await self._render_setting_revert_button(
                        ui,
                        ui_wrapper,
                        setting,
                        "restore old value",
                        setting.first_value,
                    )
                if (
                    setting.default_value != VALUE_UNAVAILABLE
                    and setting.default_value != setting.value.get()
                    and setting.default_value != setting.first_value
                ):
                    await self._render_setting_revert_button(
                        ui, ui_wrapper, setting, "set to default", setting.default_value
                    )
        except Exception as ex:
            self.error_message = f"Something went wrong in the UI for setting {error_representation_of_name}: {ex}"
            self.error_setting = setting

    async def _render_toggle_commenting_setting_column(
        self,
        ui,
        ui_wrapper,
        setting,
        comment_toggle_setting,
        error_representation_of_name,
    ):
        """Render the column for the checkbox for toggling commenting a setting"""
        checkbox_size = ui.spacing().icon_width
        if setting.is_tag:
            spacing_size = ui.spacing().icon_spacing + ui.spacing().item_spacing.x
            star_width = ui_wrapper.compute_text_width("*")
            ui.add_space(checkbox_size + spacing_size + star_width)
        else:
            if (
                ui.checkbox(egui.Mutable(setting.is_activated), "*").clicked()
                or comment_toggle_setting == setting.name
            ):
                try:
                    update_setting(setting, make_comment=not setting.is_activated)
                except Exception as ex:
                    self.error_message = f"Something went wrong trying to toggle commenting {error_representation_of_name}: {ex}"
                    self.error_setting = setting
        ui.add_space(checkbox_size)

    async def _render_error_message(self, ui, ui_wrapper, error_message, error_setting):
        async with ui.horizontal_wrapped():
            ui.strong(error_message)
            await self._render_error_copy_buttons(
                ui_wrapper, error_message, error_setting
            )

    async def _render_main_page(self, ui, total_available_height):
        """Render introductory page"""
        async with (
            egui.ScrollArea.vertical()
            .max_height(total_available_height)
            .show() as scroll_ui
        ):
            await let_user_use_page_keys_to_scroll_scroll_area(scroll_ui)
            ui.add_space(total_available_height / 4)
            async with ui.with_layout(egui.Layout.top_down(egui.Align.Center)):
                ui.heading("Welcome to the Community Setting Configuration Window")
                ui.add_space(total_available_height / 8)
                ui.label(
                    "Community provides several .talon files for configuring settings. You can use this graphical interface to edit those files without needing to learn TalonScript.\nYou may encounter unexpected behavior if you have chosen to set those settings in your own .talon files.\n\n\nThis graphical interface may not always work as intended if you have manually edited those files yourself.\nIf you run into issues with that, feel free to ask for help on the slack!"
                )
                ui.add_space(total_available_height / 8)
                ui.heading("Navigation Commands")
                ui.label(
                    "You can open a page by saying `page` and then the page name, such a saying `page popping` to open the popping settings page. You can use the ui widget for editing a setting by saying `setting` and then the setting name. You can toggle if a setting is set in a Community .talon file by saying `comment toggle` and then the name of a setting."
                )

    async def _render_error_copy_buttons(self, ui_wrapper, error_message, setting):
        """Render buttons for copying an error message including one that copies the relevant file for added context"""
        if ui_wrapper.button("copy"):
            clip.set_text(error_message)
        if ui_wrapper.button("copy with setting file"):
            path: Path = setting.path
            try:
                file_text = path.read_text()
            except OSError as ex:
                file_text = f"Error occurred trying to open the file {ex}"
            text = f"{error_message}\n\n{path.stem + path.suffix}\n\n{file_text}"
            clip.set_text(text)


manager = None


@open_gui(
    x=0.125,
    y=0.125,
    width=0.75,
    height=0.75,
    always_on_top=False,
    decorated=True,
    title="Community Settings",
    tag="user.community_settings_window",
)
async def settings_gui(ui, ui_wrapper):
    await manager.render_settings_configuration_gui(ui, ui_wrapper)


def handle_file_update(path, flags):
    if manager:
        manager.on_file_change(Path(path))
        settings_gui.refresh()


for path in RELEVANT_PATHS:
    fs.watch(path, handle_file_update)


@mod.action_class
class Actions:
    def settings_window_show():
        """Show the Community settings configuration window"""
        global manager
        if manager is None:
            manager = Manager()
        settings_gui.show()
        # the refresh is sometimes needed for this to display correctly
        settings_gui.refresh()

    def settings_window_hide():
        """Hide the Community settings configuration window"""
        global manager
        settings_gui.hide()
        manager = None

    def settings_window_open(name: str):
        """Open the page of the Community settings configuration window by name"""
        if manager is None:
            return
        manager.update_page(name)
        settings_gui.refresh()

    def settings_window_choose_setting_ui(name: str):
        """Focus or toggle the setting"""
        if manager is None:
            return
        manager.chosen_setting = name
        settings_gui.refresh()

    def settings_window_toggle_commenting_setting(name: str):
        """Toggle commenting the setting"""
        if manager is None:
            return
        manager.comment_toggle_setting = name
        settings_gui.refresh()
