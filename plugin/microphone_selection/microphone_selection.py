from talon import Context, Module, actions

from ...core.gui.gui import create_italic_text, open_gui
from ...core.user_settings import track_csv_rows

mod = Module()
ctx = Context()


DEFAULT_EXCLUDE_MICROPHONES = [
    ["Microsoft Teams Audio Device"],
    ["WebexMediaAudioDevice"],
    ["ZoomAudioDevice"],
]

EXCLUDE_MICROPHONES = set()


@track_csv_rows(
    "microphones_to_exclude.csv",
    headers=(
        "Each line has the exact name of a microphone to exclude from the microphone picker list",
    ),
    default=DEFAULT_EXCLUDE_MICROPHONES,
)
def on_microphones_to_exclude_update(rows):
    global EXCLUDE_MICROPHONES
    EXCLUDE_MICROPHONES = {row[0] for row in rows if row[0].strip()}


meta_devices = ["None", "System Default"]


def get_microphone_list():
    """
    By convention, None and System Default are listed first
    to match the Talon microphone menu.
    """

    devices = [
        device
        for device in actions.sound.microphones()
        if device not in meta_devices and device not in EXCLUDE_MICROPHONES
    ]
    devices.sort()

    return meta_devices + devices


mod.tag(
    "microphone_selection_open",
    "tag for commands that are available only when the list of microphones is visible",
)


@open_gui(refresh_period="500ms")
async def gui(ui, ui_wrapper):
    subtitle = ui_wrapper.concatenate_formatted_text(
        ("(or say: ", create_italic_text("microphone pick # "), ")")
    )
    ui_wrapper.title(
        "Click or press a number key to select a microphone",
        subtitle,
    )
    ui_wrapper.spacing()
    active_microphone = actions.sound.active_microphone()
    microphone_device_list = get_microphone_list()
    for index, item in enumerate(microphone_device_list, 1):
        if ui_wrapper.button(
            f"{f'[{index}] ' if index < 10 else ''}{item}{' — active' if item == active_microphone else ''}"
        ):
            actions.user.microphone_select(index)
    ui_wrapper.spacing()
    if ui_wrapper.command_button("[esc] microphone close"):
        actions.user.microphone_selection_hide()


@mod.action_class
class Actions:
    def microphone_selection_toggle():
        """Show GUI for choosing the Talon microphone"""

        if gui.showing:
            actions.user.microphone_selection_hide()
            return
        gui.show()
        ctx.tags = ["user.microphone_selection_open"]

    def microphone_selection_hide():
        """Hide the microphone selection GUI"""

        gui.hide()
        ctx.tags = []

    def microphone_select(index: int):
        """Selects a microphone"""
        microphone_device_list = get_microphone_list()
        if index >= 1 and index <= len(microphone_device_list):
            actions.sound.set_microphone(microphone_device_list[index - 1])
            actions.user.microphone_selection_hide()
