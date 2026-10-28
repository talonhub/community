"""This module provides UIs for configuring different kinds of settings"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import egui
from talon import actions, registry

from .rgb_conversions import (
    convert_rgb_to_hex_string,
    parse_rgb_from_hex_string,
)
from .setting_file_paths import SETTINGS_PATH
from .talon_file_output import update_setting, update_tag
from .talon_file_parsing import (
    VALUE_UNAVAILABLE,
)

DEFAULT_DESCRIPTION = "Something went wrong. Could not find the setting description."


class SettingRenderer(ABC):
    def __init__(self):
        self.should_focus = False

    @abstractmethod
    async def render(self, setting, ui):
        pass

    def focus(self):
        self.should_focus = True


@dataclass
class Setting:
    name: str
    renderer: SettingRenderer
    update_function: Callable = update_setting
    path: Path = SETTINGS_PATH
    is_tag: bool = False
    is_activated: bool = True
    value: egui.Mutable = egui.Mutable(VALUE_UNAVAILABLE)
    renders_description: bool = False
    first_value = VALUE_UNAVAILABLE
    default_value = VALUE_UNAVAILABLE

    def get_description(self):
        try:
            if self.is_tag:
                description = registry.decls.tags[self.name].desc
            else:
                description = registry.decls.settings[self.name].desc
            if not description:
                return DEFAULT_DESCRIPTION
            return description
        except Exception:
            return DEFAULT_DESCRIPTION


class ToggleSettingRenderer(SettingRenderer):
    async def render(self, setting: Setting, ui):
        response = ui.checkbox(setting.value, setting.get_description())
        if self.should_focus:
            setting.value.set(not setting.value.get())
            _focus_widget(response)
            self.should_focus = False


def create_tag_setting(name):
    return Setting(
        name,
        ToggleSettingRenderer(),
        update_tag,
        is_tag=True,
        renders_description=True,
    )


def create_boolean_setting(name):
    return Setting(
        name,
        ToggleSettingRenderer(),
        update_setting,
        renders_description=True,
    )


def _make_value_float_if_there_is_a_float_bound(value, minimum, maximum):
    if isinstance(minimum, float) or isinstance(maximum, float):
        value.set(float(value.get()))


def _focus_widget(response):
    response.request_focus()
    response.scroll_to_me(None)


class NumericSettingRenderer(SettingRenderer):
    def __init__(self, minimum, maximum, use_slider):
        super().__init__()
        self.minimum = minimum
        self.maximum = maximum
        self.use_slider = use_slider

    async def render(self, setting: Setting, ui):
        if self.use_slider:
            await self._render_slider_input(setting, ui)
        else:
            await self._render_numeric_input(setting, ui)

    async def _render_numeric_input(self, setting: Setting, ui):
        _make_value_float_if_there_is_a_float_bound(
            setting.value, self.minimum, self.maximum
        )
        response = ui.add(egui.DragValue(setting.value))
        value = setting.value.get()
        if self.minimum is not None:
            value = max(value, self.minimum)
        if self.maximum is not None:
            value = min(value, self.maximum)
        setting.value.set(value)
        if self.should_focus:
            _focus_widget(response)
            self.should_focus = False

    async def _render_slider_input(self, setting: Setting, ui):
        _make_value_float_if_there_is_a_float_bound(
            setting.value, self.minimum, self.maximum
        )
        slider = egui.Slider(setting.value, self.minimum, self.maximum)
        response = ui.add(slider)
        if self.should_focus:
            _focus_widget(response)
            # focus the numeric input instead of the slider part
            actions.key("tab")
            self.should_focus = False


def create_numeric_setting(name, minimum=None, maximum=None, use_slider=False):
    return Setting(
        name,
        NumericSettingRenderer(minimum, maximum, use_slider),
    )


class TextSettingRenderer(SettingRenderer):
    async def render(self, setting: Setting, ui):
        response = ui.add(egui.TextEdit.multiline(setting.value))
        if self.should_focus:
            _focus_widget(response)
            self.should_focus = False


def create_text_setting(name):
    return Setting(
        name,
        TextSettingRenderer(),
    )


def _compute_hexadecimal_from_color_name(name):
    color = getattr(egui.Color32, name)()
    # only get the RGB values ignoring the alpha and hexadecimal string prefix
    return color.to_hex()[1:-2]


COLOR_TO_NAME = {
    _compute_hexadecimal_from_color_name(name): name
    for name in [
        "black",
        "blue",
        "gold",
        "gray",
        "green",
        "light_blue",
        "light_green",
        "light_red",
        "magenta",
        "red",
        "white",
    ]
}


class ColorSettingRenderer(SettingRenderer):
    def __init__(self):
        super().__init__()
        self.focusing_frame = 0

    def focus(self):
        self.focusing_frame = 0
        self.should_focus = True

    async def render(self, setting: Setting, ui):
        value = setting.value.get()
        new_value = value
        async with ui.horizontal_wrapped():
            try:
                parsed_rgb = parse_rgb_from_hex_string(value)
            except ValueError:
                parsed_rgb = None
            if parsed_rgb is not None:
                # provide color picker input option
                rgb = egui.Mutable(parsed_rgb)
                egui.color_edit_button_srgb(ui, rgb)
                new_value = convert_rgb_to_hex_string(rgb.get())
            else:
                ui.label("Not valid color.")

            # allow picking color by name
            color_name = egui.Mutable("")
            # render the name of the current color if it is named
            if value in COLOR_TO_NAME:
                color_name.set(COLOR_TO_NAME[value])
            # show dropdown for picking a color name
            async with (
                egui.ComboBox(setting.name, "pick by name")
                .selected_text(color_name.get())
                .show()
            ) as combo_box:
                if combo_box.shown:
                    combo_ui = combo_box.ui
                    for name in COLOR_TO_NAME.values():
                        combo_ui.selectable_value(color_name, name, name)
            # if a color name is chosen, update the actual color
            name = color_name.get()
            if name != "":
                new_value = _compute_hexadecimal_from_color_name(name)

            # only bother updating the setting value in response to color picker and name picker inputs if the colors are actually different
            if new_value.lower() != setting.value.get().lower():
                setting.value.set(new_value)

            # allow using a text field to set the value directly
            text_response = ui.add(egui.TextEdit.singleline(setting.value))

            # allow focusing, but focus the name picker with shift tab as a temporary workaround for not being able to focus the combo box directly
            if self.should_focus:
                match self.focusing_frame:
                    case 0:
                        _focus_widget(text_response)
                    case 1:
                        actions.key("shift-tab")
                    case 2:
                        actions.key("enter")
                        self.should_focus = False
                self.focusing_frame += 1


def create_color_picker_setting(name):
    return Setting(
        name,
        ColorSettingRenderer(),
    )


class DiscretSettingRenderer(SettingRenderer):
    def __init__(self, choices, is_numeric):
        super().__init__()
        self.focusing_frame = 0
        self.choices = choices
        self.is_numeric = is_numeric

    def focus(self):
        self.focusing_frame = 0
        self.should_focus = True

    async def render(self, setting: Setting, ui):
        async with ui.horizontal():
            async with (
                egui.ComboBox(setting.name, "pick option")
                .selected_text(str(setting.value.get()))
                .show()
            ) as combo_box:
                if combo_box.shown:
                    combo_ui = combo_box.ui
                    for value, text in self.choices:
                        combo_ui.selectable_value(setting.value, value, text)
            if self.is_numeric:
                response = ui.add(egui.DragValue(setting.value))
            else:
                response = ui.add(egui.TextEdit.singleline(setting.value))

            if self.should_focus:
                match self.focusing_frame:
                    case 0:
                        _focus_widget(response)
                    case 1:
                        actions.key("shift-tab")
                    case 2:
                        actions.key("enter")
                        self.should_focus = False
                self.focusing_frame += 1


def create_discrete_choices_setting(name, choices, is_numeric=False):
    """Choices is an iterable of tuples with the value and text of each option respectively"""
    return Setting(
        name,
        DiscretSettingRenderer(choices, is_numeric),
    )
