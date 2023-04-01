from talon import Module, actions, app, imgui
from talon.lib import cubeb

ctx = cubeb.Context()
mod = Module()


microphone_device_list = []


# by convention, None and System Default are listed first
# to match the Talon context menu.
def update_microphone_list():
    global microphone_device_list
    microphone_device_list = ["None", "System Default"]

    # On Windows, it's presently necessary to check the state, or
    # we will get any and every microphone that was ever connected.
    devices = [
        dev.name for dev in ctx.inputs() if dev.state == cubeb.DeviceState.ENABLED
    ]

    devices.sort()
    microphone_device_list += devices


def devices_changed(device_type):
    update_microphone_list()


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Select a Microphone")
    gui.line()
    for index, item in enumerate(microphone_device_list, 1):
        if gui.button(f"{index}. {item}"):
            actions.user.microphone_select(index)

    gui.spacer()
    if gui.button("Microphone close"):
        actions.user.microphone_selection_hide()


@mod.action_class
class Actions:
    def microphone_selection_toggle():
        """Show GUI for choosing the Talon microphone"""
        if gui.showing:
            gui.hide()
        else:
            update_microphone_list()
            gui.show()

    def microphone_selection_hide():
        """Hide the microphone selection GUI"""
        gui.hide()

    def microphone_select(index: int):
        """Selects a micropohone"""
        if 1 <= index and index <= len(microphone_device_list):
            actions.sound.set_microphone(microphone_device_list[index - 1])
            app.notify(f"Activating microphone: {microphone_device_list[index - 1]}")
            gui.hide()


def on_ready():
    ctx.register("devices_changed", devices_changed)
    update_microphone_list()


app.register("ready", on_ready)
