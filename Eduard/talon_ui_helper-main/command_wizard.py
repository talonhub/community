"""
Actions related to building voice commands.
"""

import os
import datetime

from talon import Module, Context, actions, ui, imgui

from .overlays import ImageSelectorOverlay, BlobBoxOverlay
from .mouse_helper import get_image_template_directory


mod = Module()
mod.tag("command_wizard_showing", desc="The command wizard is showing")
ctx = Context()


def save_image_template(image):
    """
    Saves the given image to the image templates folder and returns the generated name.58
    """

    unique_filename = \
        str(datetime.datetime.now().date()) + '_' + \
        str(datetime.datetime.now().time()).replace(':', '.') + \
        ".png"

    templates_directory = get_image_template_directory()
    full_filename = os.path.join(templates_directory, unique_filename)

    if not os.path.exists(templates_directory):
        os.mkdir(templates_directory)

    image.write_file(full_filename)

    return unique_filename


def handle_image_click_builder(result):
    """
    Result handler for the image click command builder.
    """
    if result is None:
        return

    filename = save_image_template(result["image"])
    index = result["index"]

    offset_bit = ""
    if result["offset"]:
        offset_bit = ", ".join([""] + list(map(lambda x: str(int(x)), result["offset"])))

    command = "\n".join([
        "",
        ":",
        "    user.mouse_helper_position_save()",
        f'    user.mouse_helper_move_image_relative("{filename}", {index}{offset_bit})',
        "    sleep(0.05)",
        "    mouse_click(0)",
        "    sleep(0.05)",
        "    user.mouse_helper_position_restore()",
    ])
    actions.clip.set_text(command)
    actions.app.notify("Copied new command to clipboard")


def handle_multi_image_builder(result):
    """
    Result handler for the multi image marker command builder.
    """
    if result is None:
        return

    filename = save_image_template(result["image"])

    offset_bit = ""
    if result["offset"]:
        offset_bit = ", ".join([""] + list(map(lambda x: str(int(x)), result["offset"])))

    command = "\n".join([
        "",
        ":",
        f'    matches = user.mouse_helper_find_template_relative("{filename}"{offset_bit})',
        "    user.marker_ui_show(matches)",
    ])
    actions.clip.set_text(command)
    actions.app.notify("Copied new command to clipboard")


def handle_blob_detect_builder(result):
    """
    Result handler for the blob detect command builder.
    """
    if result is None:
        return

    active_rectangle = ui.active_window().rect
    def calculate_offset(position, minimum, width):
        # Split each axis into two to determine which side of the screen
        # the coordinate is offset from
        maximum = minimum + width
        split = (minimum + maximum) / 2
        if position > split:
            return str(position - maximum)
        else:
            return str(position - minimum)

    offsets = " ".join([
        calculate_offset(result.x, active_rectangle.x, active_rectangle.width),
        calculate_offset(result.y, active_rectangle.y, active_rectangle.height),
        calculate_offset(result.x + result.width, active_rectangle.x, active_rectangle.width),
        calculate_offset(result.y + result.height, active_rectangle.y, active_rectangle.height),
    ])

    command = "\n".join([
        "",
        ":",
        f'    bounding_rectangle = user.mouse_helper_calculate_relative_rect("{offsets}", "active_window")',
        f'    user.mouse_helper_blob_picker(bounding_rectangle)',
    ])
    actions.clip.set_text(command)
    actions.app.notify("Copied new command to clipboard")


command_wizards = [
    (
        "Click a single image on the screen",
        ImageSelectorOverlay,
        handle_image_click_builder,
        (
            "Select a region of the screen as an image to find in your voice command "
            "then press enter to confirm your selection. Press escape to cancel.\n\n"
            "After selecting and before enter, optionally right click to define an "
            "offset from the selected region. This will be clicked instead of the "
            "center of the region."
        )
    ),
    (
        "Show markers on all image matches on screen",
        ImageSelectorOverlay,
        handle_multi_image_builder,
        (
            "Select a region of the screen as an image to find in your voice command "
            "then press enter to confirm your selection. Press escape to cancel.\n\n"
            "After selecting and before enter, optionally right click to define an "
            "offset from the selected region. This will be clicked instead of the "
            "center of the region."
        )
    ),
    (
        "Find items in a box to click",
        BlobBoxOverlay,
        handle_blob_detect_builder,
        (
            "Select a region of the active window to use in your voice command then press "
            "enter to confirm your selection. Press escape to cancel.\n\n"
            "When drawing a box wider than tall, the first row of pixels will be "
            "considered background color. When the box is taller than wide the first "
            "column of pixels will be considered background color.\n\n"
            "The background color will be used to detect clickable regions in the area "
            "you selected. "
        )
    )
]

existing_overlay = None


def open_overlay(index):
    global existing_overlay

    builder_picker_toggle(False)

    if existing_overlay:
        existing_overlay.destroy()

    _, overlay, handler, help = command_wizards[index]
    existing_overlay = overlay(handler, text=help)


@imgui.open(y=0)
def builder_picker(gui: imgui.GUI):
    t = gui.text("Choose the command type that you would like to build:")
    gui.spacer()

    for i, (text, _, _, _) in enumerate(command_wizards):
        gui.text(text)
        if gui.button(f"Choose {i+1}"):
            open_overlay(i)
        gui.spacer()

    if gui.button("Command wizard hide"):
        builder_picker_toggle(False)


def builder_picker_toggle(visible: bool):
    if visible:
        builder_picker.show()
        ctx.tags = ["user.command_wizard_showing"]
    else:
        builder_picker.hide()
        ctx.tags = []


@mod.action_class
class CommandWizardActions:
    """
    Actions related to the command builder wizard.
    """

    def command_wizard_show():
        """
        Brings up the command wizard UI
        """

        builder_picker_toggle(True)

    def command_wizard_hide():
        """
        Closes the command wizard UI
        """

        builder_picker_toggle(False)

    def command_wizard_choose_option(option: int):
        """
        Chooses one of the command wizards
        """

        open_overlay(option - 1)
