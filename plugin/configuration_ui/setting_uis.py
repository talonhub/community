"""This module provides UIs for configuring different kinds of settings"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import egui
from talon import actions, registry

from .rgb_conversions import (
    convert_rgb_to_string,
    is_valid_hexadecimal_rgb,
    parse_rgb_from_string,
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


async def draw_toggle(setting: Setting, ui, is_setting_chosen):
    response = ui.checkbox(setting.value, setting.get_description())
    if is_setting_chosen:
        setting.value.set(not setting.value.get())
        focus_widget(response, True)


def create_tag_setting(name):
    return Setting(
        name,
        draw_toggle,
        update_tag,
        is_tag=True,
        draws_description=True,
    )


def create_boolean_setting(name):
    return Setting(
        name,
        draw_toggle,
        update_setting,
        draws_description=True,
    )


def make_value_float_if_there_is_a_float_bound(value, minimum, maximum):
    if (isinstance(minimum, float) or isinstance(maximum, float)) and isinstance(
        value.get(), int
    ):
        value.set(float(value.get()))


def focus_widget(response, is_setting_chosen):
    if is_setting_chosen:
        response.request_focus()
        response.scroll_to_me(None)


async def draw_numeric_input(setting: Setting, ui, minimum, maximum, is_setting_chosen):
    make_value_float_if_there_is_a_float_bound(setting.value, minimum, maximum)
    response = ui.add(egui.DragValue(setting.value))
    value = setting.value.get()
    if minimum is not None and value < minimum:
        setting.value.set(minimum)
    if maximum is not None and value > maximum:
        setting.value.set(maximum)
    focus_widget(response, is_setting_chosen)


async def draw_slider_input(setting: Setting, ui, minimum, maximum, is_setting_chosen):
    make_value_float_if_there_is_a_float_bound(setting.value, minimum, maximum)
    slider = egui.Slider(setting.value, minimum, maximum)
    response = ui.add(slider)
    focus_widget(response, is_setting_chosen)


async def draw_single_line_text_input(setting: Setting, ui, is_setting_chosen):
    response = ui.add(egui.TextEdit.singleline(setting.value))
    focus_widget(response, is_setting_chosen)


async def draw_multiline_text_input(setting: Setting, ui, is_setting_chosen):
    response = ui.add(egui.TextEdit.multiline(setting.value))
    focus_widget(response, is_setting_chosen)


def create_numeric_setting(name, minimum=None, maximum=None, use_slider=False):
    ui_function = draw_slider_input if use_slider else draw_numeric_input
    return Setting(
        name,
        lambda setting, ui, is_setting_chosen: ui_function(
            setting, ui, minimum, maximum, is_setting_chosen
        ),
    )


def create_text_setting(name, is_multiline=False):
    ui_function = (
        draw_multiline_text_input if is_multiline else draw_single_line_text_input
    )
    return Setting(
        name,
        ui_function,
    )


COLOR_NAMES = [
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


def compute_hexadecimal_from_color_name(name):
    function = getattr(egui.Color32, name)
    color = function()
    return color.to_hex()[1:-2]


async def draw_color_picker_input(setting: Setting, ui, is_setting_chosen):
    value = setting.value.get()
    new_value = value
    is_valid_rgb = is_valid_hexadecimal_rgb(value)
    async with ui.horizontal_wrapped():
        if is_valid_rgb:
            red, green, blue = parse_rgb_from_string(value)
            rgba = egui.Rgba.from_srgba_unmultiplied(red, green, blue, 255)
            rgb = egui.Mutable([rgba.r, rgba.g, rgba.b])
            egui.color_edit_button_rgb(ui, rgb)
            out_rgba = egui.Rgba.from_rgb(*rgb.get())
            new_value = convert_rgb_to_string(out_rgba.to_srgba_unmultiplied()[:3])
        else:
            ui.label("Not valid color.")

        color_name = egui.Mutable("")
        for name in COLOR_NAMES:
            if compute_hexadecimal_from_color_name(name) == value:
                color_name.set(name)
                break
        async with (
            egui.ComboBox(setting.name, "pick by name")
            .selected_text(color_name.get())
            .show()
        ) as combo_box:
            if combo_box.shown:
                combo_ui = combo_box.ui
                for name in COLOR_NAMES:
                    combo_ui.selectable_value(color_name, name, name)
        name = color_name.get()
        if name != "":
            new_value = compute_hexadecimal_from_color_name(name)

        if new_value != setting.value.get().lower():
            setting.value.set(new_value)
        text_response = ui.add(egui.TextEdit.singleline(setting.value))
        if is_setting_chosen:
            focus_widget(text_response, True)
            actions.key("shift-tab")


def create_color_picker_setting(name):
    return Setting(
        name, draw_color_picker_input, post_chosen_action=lambda: actions.key("enter")
    )


async def draw_discreet_choices_input(
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
            focus_widget(response, True)
            actions.key("shift-tab")


def create_discreet_choices_setting(name, choices, is_numeric=False):
    """Choices is an iterable of tuples with the value and text of each option respectively"""
    return Setting(
        name,
        lambda setting, ui, is_chosen: draw_discreet_choices_input(
            setting, ui, choices, is_chosen, is_numeric
        ),
        post_chosen_action=lambda: actions.key("enter"),
    )
