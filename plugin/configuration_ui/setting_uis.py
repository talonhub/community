"""This module provides UIs for configuring different kinds of settings"""

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
from .talon_file_handling import (
    VALUE_UNAVAILABLE,
    update_setting,
    update_tag,
)

DEFAULT_DESCRIPTION = "Something went wrong. Could not find the setting description."


@dataclass
class Setting:
    name: str
    draw: Callable
    update_function: Callable = update_setting
    path: Path = SETTINGS_PATH
    is_tag: bool = False
    is_activated: bool = True
    value: egui.Mutable = egui.Mutable(VALUE_UNAVAILABLE)
    draws_description: bool = False
    post_chosen_action: Callable | None = None

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


async def _draw_toggle(setting: Setting, ui, is_setting_chosen):
    response = ui.checkbox(setting.value, setting.get_description())
    if is_setting_chosen:
        setting.value.set(not setting.value.get())
        _focus_widget(response)


def create_tag_setting(name):
    return Setting(
        name,
        _draw_toggle,
        update_tag,
        is_tag=True,
        draws_description=True,
    )


def create_boolean_setting(name):
    return Setting(
        name,
        _draw_toggle,
        update_setting,
        draws_description=True,
    )


def _make_value_float_if_there_is_a_float_bound(value, minimum, maximum):
    if isinstance(minimum, float) or isinstance(maximum, float):
        value.set(float(value.get()))


def _focus_widget(response):
    response.request_focus()
    response.scroll_to_me(None)


async def _draw_numeric_input(
    setting: Setting, ui, minimum, maximum, is_setting_chosen
):
    _make_value_float_if_there_is_a_float_bound(setting.value, minimum, maximum)
    response = ui.add(egui.DragValue(setting.value))
    value = setting.value.get()
    if minimum is not None:
        value = max(value, minimum)
    if maximum is not None:
        value = min(value, maximum)
    setting.value.set(value)
    if is_setting_chosen:
        _focus_widget(response)


async def _draw_slider_input(setting: Setting, ui, minimum, maximum, is_setting_chosen):
    _make_value_float_if_there_is_a_float_bound(setting.value, minimum, maximum)
    slider = egui.Slider(setting.value, minimum, maximum)
    response = ui.add(slider)
    if is_setting_chosen:
        _focus_widget(response)
        # focus the numeric input instead of the slider part 
        actions.key("tab")


async def _draw_multiline_text_input(setting: Setting, ui, is_setting_chosen):
    response = ui.add(egui.TextEdit.multiline(setting.value))
    if is_setting_chosen:
        _focus_widget(response)


def create_numeric_setting(name, minimum=None, maximum=None, use_slider=False):
    ui_function = _draw_slider_input if use_slider else _draw_numeric_input
    return Setting(
        name,
        lambda setting, ui, is_setting_chosen: ui_function(
            setting, ui, minimum, maximum, is_setting_chosen
        ),
    )


def create_text_setting(name):
    return Setting(
        name,
        _draw_multiline_text_input,
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


async def _draw_color_picker_input(setting: Setting, ui, is_setting_chosen):
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
        if is_setting_chosen:
            _focus_widget(text_response)
            actions.key("shift-tab")


def create_color_picker_setting(name):
    return Setting(
        name, _draw_color_picker_input, post_chosen_action=lambda: actions.key("enter")
    )


async def _draw_discrete_choices_input(
    setting: Setting, ui, choices, is_chosen, is_numeric
):
    async with ui.horizontal():
        async with (
            egui.ComboBox(setting.name, "pick option")
            .selected_text(str(setting.value.get()))
            .show()
        ) as combo_box:
            if combo_box.shown:
                combo_ui = combo_box.ui
                for value, text in choices:
                    combo_ui.selectable_value(setting.value, value, text)
        if is_numeric:
            response = ui.add(egui.DragValue(setting.value))
        else:
            response = ui.add(egui.TextEdit.singleline(setting.value))
        if is_chosen:
            _focus_widget(response)
            actions.key("shift-tab")


def create_discrete_choices_setting(name, choices, is_numeric=False):
    """Choices is an iterable of tuples with the value and text of each option respectively"""
    return Setting(
        name,
        lambda setting, ui, is_chosen: _draw_discrete_choices_input(
            setting, ui, choices, is_chosen, is_numeric
        ),
        post_chosen_action=lambda: actions.key("enter"),
    )
