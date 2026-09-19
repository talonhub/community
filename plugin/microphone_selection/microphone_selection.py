from talon import Context, Module, actions, cron, imgui

mod = Module()
ctx = Context()


EXCLUDE_MICROPHONES = {
    "Microsoft Teams Audio Device",
    "WebexMediaAudioDevice",
    "ZoomAudioDevice",
}

microphone_device_list = []
update_microphone_cron_job = None


def update_microphone_list():
    global microphone_device_list
    # By convention, None and System Default are listed first
    # to match the Talon microphone menu.
    meta_devices = ["None", "System Default"]

    devices = [
        device
        for device in actions.sound.microphones()
        if device not in meta_devices and device not in EXCLUDE_MICROPHONES
    ]
    devices.sort()

    microphone_device_list = meta_devices + devices


def devices_changed(device_type):
    update_microphone_list()


mod.tag(
    "microphone_selection_open",
    "tag for commands that are available only when the list of microphones is visible",
)


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Click or press a number key to select a microphone")
    gui.text("(or say “microphone pick #”)")
    gui.line()
    gui.text("Microphone list updates every 5 seconds")
    gui.spacer()
    active_microphone = actions.sound.active_microphone()
    for index, item in enumerate(microphone_device_list, 1):
        if gui.button(
            f"{f'[{index}] ' if index < 10 else ''}{item}{' — active' if item == active_microphone else ''}"
        ):
            actions.user.microphone_select(index)
    gui.spacer()
    if gui.button("[esc] microphone close"):
        actions.user.microphone_selection_hide()


@mod.action_class
class Actions:
    def microphone_selection_toggle():
        """Show GUI for choosing the Talon microphone"""
        global update_microphone_cron_job

        if gui.showing:
            actions.user.microphone_selection_hide()
            return
        update_microphone_list()
        gui.show()
        ctx.tags = ["user.microphone_selection_open"]
        update_microphone_cron_job = cron.interval("5s", update_microphone_list)

    def microphone_selection_hide():
        """Hide the microphone selection GUI"""
        global update_microphone_cron_job

        gui.hide()
        ctx.tags = []
        cron.cancel(update_microphone_cron_job)
        update_microphone_cron_job = None

    def microphone_select(index: int):
        """Selects a microphone"""
        if index >= 1 and index <= len(microphone_device_list):
            actions.sound.set_microphone(microphone_device_list[index - 1])
            actions.user.microphone_selection_hide()
