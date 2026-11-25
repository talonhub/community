import logging
from pathlib import Path

import egui
from talon import Context, Module, actions, clip, fs, registry

from ...core.gui.gui import (
    UIWrapper,
    create_italic_text,
    let_user_use_page_keys_to_scroll_scroll_area,
    open_gui,
)
from .pages import Page, create_pages
from .setting_file_paths import RELEVANT_PATHS
from .setting_uis import Setting
from .talon_file_output import update_setting
from .talon_file_parsing import (
    VALUE_UNAVAILABLE,
    SettingFileSettingInformation,
    SettingsParser,
)

mod = Module()
ctx = Context()

mod.tag(
    "community_settings_window_open",
    desc="Community settings configuration window is open",
)
mod.list(
    "community_settings_window_page",
    desc="The name of a page in the Community settings window",
)


def _update_displayed_setting_information(
    setting: Setting, new_info: SettingFileSettingInformation
):
    """Update displayed setting state using information from the containing file"""
    setting.value.set(new_info.value)
    setting.is_activated = new_info.is_activated

    if setting.first_value is VALUE_UNAVAILABLE:
        setting.first_value = new_info.value

    if not setting.is_tag and setting.default_value is VALUE_UNAVAILABLE:
        try:
            declaration = registry.decls.settings[setting.name]
        except KeyError:
            return
        default = declaration.default
        if isinstance(default, declaration.type):
            setting.default_value = default


def _handle_setting_parsing_error(
    setting: Setting, parser: SettingsParser, file_name: str
):
    error_message = ""
    if setting.name in parser.get_duplicates(setting.is_tag):
        error_message = f"It appears more than once in {file_name}."
    setting.handle_value_unavailable(error_message)


def compute_readable_name(setting_name: str, page_prefix: str):
    words = []
    if page_prefix and setting_name.startswith(page_prefix):
        name = setting_name.removeprefix(page_prefix)
    else:
        prefix, name = setting_name.split(".")
        if prefix != "user":
            words = [prefix]
    words.extend(name.split("_"))
    # this is doing title formatting and not actually capitalizing all words
    return actions.user.formatted_text(" ".join(words), "CAPITALIZE_ALL_WORDS")


MAIN_PAGE_NAME = "Main"


class Manager:
    """Responsible for the configuration UI. Organizes settings into pages, updates settings in response to user input, and updates the rendered state in response to the underlying files changing."""

    __slots__ = (
        "page",
        "pages",
        "error_setting",
        "chosen_setting_number",
        "_ui",
        "error_message",
        "_times_to_refresh",
        "_ui_wrapper",
    )

    pages: dict[str, Page]
    page: str
    error_message: str
    error_setting: Setting | None
    _ui: egui.Ui
    _ui_wrapper: UIWrapper
    chosen_setting_number: int | None
    _times_to_refresh: int

    def __init__(self):
        pages = create_pages()
        self.pages = {page.title: page for page in pages}
        self.page = MAIN_PAGE_NAME
        # use the change handling logic for handling the initial file states
        for path in RELEVANT_PATHS:
            self.on_file_change(path)
        self.error_message = ""
        self.error_setting = None
        ctx.lists["user.community_settings_window_page"] = [
            page.title for page in pages
        ] + [MAIN_PAGE_NAME]

        self.chosen_setting_number = None
        self._times_to_refresh = 0

    def handle_just_opened(self):
        self._times_to_refresh = 10

    def update_page(self, page_name):
        self.page = page_name

    def _get_settings_at_path(self, path):
        return (
            setting
            for page in self.pages.values()
            for setting in page.settings
            if setting.path == path
        )

    def on_file_change(self, path):
        """Update setting values rendered in response to the .talon file at path changing"""
        try:
            parser = SettingsParser(path)
        except FileNotFoundError:
            parser = None

        for setting in self._get_settings_at_path(path):
            file_name = setting.path.stem + setting.path.suffix
            if not parser:
                setting.handle_value_unavailable(f"{file_name} was not found.")
            elif new_info := parser.get_setting_information(
                setting.name, setting.is_tag
            ):
                _update_displayed_setting_information(setting, new_info)
            else:
                _handle_setting_parsing_error(setting, parser, file_name)

    async def render_settings_configuration_gui(self, ui, ui_wrapper):
        # set these at the start to avoid a situation where these are set in the middle of this function leading to an invalid state
        chosen_setting = self.chosen_setting_number
        old_error_message = self.error_message

        # if the user chose a valid setting to focus, focus it
        if chosen_setting is not None and self._is_setting_number_valid(chosen_setting):
            setting = self.pages[self.page].settings[chosen_setting - 1]
            if setting.is_activated:
                setting.renderer.focus()

        self._ui = ui
        self._ui_wrapper = ui_wrapper

        # put the page navigation on the left and the actual page on the right
        total_available_height = ui.available_height()
        async with self._ui.horizontal():
            await self._render_page_navigation(total_available_height)

            # compute the space for the page
            available_width = self._ui.available_width()
            interaction_region_space = egui.Vec2(
                available_width, total_available_height
            )

            # render the page
            async with (
                self._ui.allocate_ui(interaction_region_space),
                self._ui.ui.vertical(),
            ):
                await self._render_current_page(
                    total_available_height,
                )

        # clean up state
        if chosen_setting is not None:
            self.chosen_setting_number = None
            settings_gui.refresh()
        if old_error_message != self.error_message:
            settings_gui.refresh()

        # the refresh and focus is sometimes needed for this to display correctly
        if self._times_to_refresh > 0:
            self._times_to_refresh -= 1
            settings_gui.refresh()
            settings_gui.focus()

    async def _render_page_navigation(self, total_available_height):
        async with self._ui.vertical():
            for page in self.pages:
                if self._ui.selectable_label(
                    page == self.page, create_italic_text(f"Page {page}")
                ).clicked():
                    self.update_page(page)
            if self._ui.selectable_label(
                self.page == MAIN_PAGE_NAME, create_italic_text("Page Main")
            ).clicked():
                self.update_page(MAIN_PAGE_NAME)
            self._ui_wrapper.spacing()
            if self._ui_wrapper.button(create_italic_text("settings close")):
                actions.user.settings_window_hide()

            self._ui.add_space(total_available_height - self._ui.min_size().y)
        self._ui.separator()

    async def _render_current_page(
        self,
        total_available_height,
    ):
        if self.page == MAIN_PAGE_NAME:
            await self._render_main_page(total_available_height)
            return

        if self.error_message:
            await self._render_error_message(self.error_message, self.error_setting)
        self._ui.add_space(10)
        await self._render_configuration_page(
            total_available_height,
        )

    async def _render_configuration_page(
        self,
        total_available_height,
    ):
        page = self.pages[self.page]

        async with (
            egui.ScrollArea.vertical()
            .max_height(total_available_height)
            .show() as scroll_ui
        ):
            await let_user_use_page_keys_to_scroll_scroll_area(scroll_ui)

            self._ui.strong(page.title)
            if page.description:
                self._ui.label(page.description)
            self._ui.separator()
            self._ui.add_space(5)
            async with self._ui.group():
                command_instructions_text = self._ui_wrapper.concatenate_formatted_text(
                    (
                        create_italic_text("setting <number>"),
                        ': use the input for editing the setting, such as by saying "setting one".\n',
                        create_italic_text("comment toggle <number>"),
                        ': toggle if the setting is configured in a Community .talon file, such as by saying "comment toggle one".\n',
                        create_italic_text("page up"),
                        " / ",
                        create_italic_text("page down"),
                        " /",
                    )
                )
                async with self._ui.horizontal_wrapped():
                    self._ui.label(command_instructions_text)
                    # this section will not wrap properly, but without this the layout gets messed up with some text sizes
                    # other parts of this window will have to be made more wrapping friendly before this matters
                    async with self._ui.horizontal():
                        await self._ui_wrapper.render_key(
                            "PgUp", "Page Up", "scroll this window up"
                        )
                        self._ui.label("/")
                        await self._ui_wrapper.render_key(
                            "PgDn", "Page Down", "scroll this window down"
                        )
                        self._ui.label(": scroll this window")
            self._ui_wrapper.spacing()
            self._ui.label(
                "* toggle configuring that setting in a Community .talon file"
            )
            self._ui.separator()

            for i, setting in enumerate(page.settings):
                await self._render_setting_row(
                    setting,
                    page,
                    i + 1,
                )
                self._ui.separator()

    async def _render_setting_row(self, setting, page, setting_number):
        """Render the row for a setting"""
        readable_name = compute_readable_name(setting.name, page.prefix)
        error_representation_of_name = f"{readable_name} ({setting.name})"
        async with self._ui.horizontal():
            await self._render_toggle_commenting_setting_column(
                setting,
                error_representation_of_name,
            )
            async with self._ui.with_layout(egui.Layout.right_to_left(egui.Align.TOP)):
                async with self._ui.vertical():
                    self._ui.strong(f"{setting_number}: {readable_name}")
                    self._ui.weak(setting.name)
                    self._ui.add_space(5)
                    if not setting.renderer.renders_description:
                        self._ui.label(setting.description)
                    if setting.value.get() is VALUE_UNAVAILABLE:
                        type_used = setting.implementation_type_description
                        error_prefix = f"Something went wrong with the {type_used} {error_representation_of_name}: "
                        if setting.value_unavailable_error_message:
                            error_message = setting.value_unavailable_error_message
                        else:
                            error_message = (
                                "It could not be found or could not be parsed."
                            )
                        await self._render_error_message(
                            error_prefix + error_message, setting
                        )
                    else:
                        await self._render_settings_ui(
                            setting,
                            error_representation_of_name,
                        )
                self._ui.separator()

    async def _render_setting_revert_button(self, setting, button_text, revert_value):
        async with self._ui.group(), self._ui.horizontal_wrapped():
            if self._ui_wrapper.button(button_text):
                setting.update_function(setting, revert_value)
            self._ui.label(str(revert_value))

    async def _render_settings_ui(self, setting, error_representation_of_name):
        """Render the ui for changing the setting"""
        old_value = setting.value.get()
        try:
            async with self._ui.add_enabled_ui(setting.is_activated or setting.is_tag):
                # render the main input for updating the setting
                await setting.renderer.render(setting, self._ui)
                value = setting.value.get()
                if old_value != value:
                    setting.update_function(setting, value)

                # let the user revert the setting to the old or default value
                if setting.first_value != setting.value.get():
                    await self._render_setting_revert_button(
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
                        setting, "set to default", setting.default_value
                    )
        except Exception as ex:
            type_used = setting.implementation_type_description
            error_prefix = f"Something went wrong in the UI for {type_used} {error_representation_of_name}"
            await self._render_error_message(f"{error_prefix}: {ex}", setting)
            logging.exception(error_prefix)

    async def _render_toggle_commenting_setting_column(
        self,
        setting,
        error_representation_of_name,
    ):
        """Render the column for the checkbox for toggling commenting a setting"""
        checkbox_size = self._ui.spacing().icon_width
        if setting.is_tag:
            spacing_size = (
                self._ui.spacing().icon_spacing + self._ui.spacing().item_spacing.x
            )
            star_width = self._ui_wrapper.compute_text_width("*")
            self._ui.add_space(checkbox_size + spacing_size + star_width)
        else:
            if self._ui.checkbox(egui.Mutable(setting.is_activated), "*").clicked():
                self._toggle_setting_comment(setting, error_representation_of_name)
        self._ui.add_space(checkbox_size)

    def _toggle_setting_comment(self, setting, error_representation_of_name):
        try:
            update_setting(setting, make_comment=setting.is_activated)
        except Exception as ex:
            message_prefix = f"Something went wrong trying to toggle commenting {error_representation_of_name}"
            self.error_message = f"{message_prefix}: {ex}"
            self.error_setting = setting
            logging.exception(message_prefix)

    async def _render_error_message(self, error_message, error_setting):
        async with self._ui.vertical():
            await self._ui_wrapper.warning_text(error_message)
            async with self._ui.horizontal_wrapped():
                await self._render_error_copy_buttons(error_message, error_setting)

    async def _render_main_page(self, total_available_height):
        """Render introductory page"""
        async with (
            egui.ScrollArea.vertical()
            .max_height(total_available_height)
            .show() as scroll_ui
        ):
            await let_user_use_page_keys_to_scroll_scroll_area(scroll_ui)
            self._ui.add_space(total_available_height / 4)
            async with self._ui.with_layout(egui.Layout.top_down(egui.Align.Center)):
                self._ui.heading(
                    "Welcome to the Community Setting Configuration Window"
                )
                self._ui.add_space(total_available_height / 8)
                self._ui.label(
                    "Community provides several .talon files for configuring settings. You can use this window to edit those files without needing to learn TalonScript.\nYou may encounter unexpected behavior if you have chosen to set those settings in your own .talon files.\n\n\nThis window may not always work as intended if you have manually edited those files yourself.\nIf you run into issues with that, feel free to ask for help on the Slack!"
                )

    async def _render_error_copy_buttons(self, error_message, setting):
        """Render buttons for copying an error message including one that copies the relevant file for added context"""
        if self._ui_wrapper.button("copy"):
            clip.set_text(error_message)
        if self._ui_wrapper.button("copy with setting file"):
            path: Path = setting.path
            try:
                file_text = path.read_text(encoding="utf-8")
            except OSError as ex:
                file_text = f"Error occurred trying to open the file {ex}"
            text = f"{error_message}\n\n{path.stem + path.suffix}\n\n{file_text}"
            clip.set_text(text)

    def toggle_commenting_setting_by_number(self, number: int):
        """Toggle commenting a setting on the current page by its number"""
        if not self._is_setting_number_valid(number):
            return
        page = self.pages[self.page]
        setting = page.settings[number - 1]
        if setting.is_tag:
            return
        readable_name = compute_readable_name(setting.name, page.prefix)
        self._toggle_setting_comment(setting, readable_name)

    def _is_setting_number_valid(self, number: int) -> bool:
        if number < 1:
            return False
        page = self.pages.get(self.page)
        if not page:
            return False
        return len(page.settings) >= number


manager = None


def on_close_cleanup():
    global manager
    manager = None


@open_gui(
    width=0.75,
    height=0.75,
    always_on_top=False,
    decorated=True,
    title="Community Settings",
    tag="user.community_settings_window_open",
    on_close=on_close_cleanup,
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
        manager.handle_just_opened()
        settings_gui.show()

    def settings_window_hide():
        """Hide the Community settings configuration window"""
        settings_gui.hide()

    def settings_window_open(name: str):
        """Open the page of the Community settings configuration window by name"""
        if manager is None:
            return
        manager.update_page(name)
        settings_gui.refresh()

    def settings_window_choose_setting_ui(number: int):
        """Focus or toggle the setting by number"""
        settings_gui.focus()
        if manager is None:
            return
        manager.chosen_setting_number = number
        settings_gui.refresh()

    def settings_window_toggle_commenting_setting(number: int):
        """Toggle commenting the setting by number"""
        settings_gui.focus()
        if manager is None:
            return
        manager.toggle_commenting_setting_by_number(number)
        settings_gui.refresh()
