from talon import Module, actions, app, imgui
from talon.lib import cubeb
from subprocess import call
import os

ctx = cubeb.Context()
mod = Module()

if app.platform == "windows":
    previous_mic = "Microphone (d:vice MMA-A)"
else:
    previous_mic = "d:vice MMA-A"
# previous_mic = "Krisp Microphone (Krisp)"
microphone_device_list = []
speaker_device_list = []
# by convention, None and System Default are listed first
# to match the Talon context menu.
def update_microphone_list():
    global microphone_device_list, speaker_device_list
    microphone_device_list = ["None", "System Default"]

    # On Windows, it's presently necessary to check the state, or
    # we will get any and every microphone that was ever connected.
    devices = [
        dev.name for dev in ctx.inputs() if dev.state == cubeb.DeviceState.ENABLED
    ]
    speaker_device_list = [
        dev.name for dev in ctx.outputs() if dev.state == cubeb.DeviceState.ENABLED
    ]
    speaker_device_list.sort()
    devices.sort()
    microphone_device_list += devices


def devices_changed(device_type):
    update_microphone_list()


@imgui.open()
def gui_microphone(gui: imgui.GUI):
    gui.text("Select a Microphone")
    gui.line()
    for index, item in enumerate(microphone_device_list, 1):
        if gui.button("{}. {}".format(index, item)):
            actions.user.microphone_select(index)


@imgui.open()
def gui_speaker(gui: imgui.GUI):
    gui.text("Select a speaker")
    gui.line()
    for index, item in enumerate(speaker_device_list, 1):
        if gui.button("{}. {}".format(index, item)):
            actions.user.speaker_select(index)


@mod.action_class
class Actions:
    def microphone_selection_toggle():
        """"""
        if gui_microphone.showing:
            gui_microphone.hide()
        else:
            update_microphone_list()
            gui_microphone.show()

    def microphone_select(index: int):
        """Selects a micropohone"""
        if 1 <= index and index <= len(microphone_device_list):

            actions.speech.set_microphone(microphone_device_list[index - 1])
            app.notify(
                "Activating microphone: {}".format(microphone_device_list[index - 1])
            )
            gui_microphone.hide()

    def microphone_toggle():
        """Toggles the microphone and speech"""
        global previous_mic
        if actions.speech.enabled():
            actions.speech.set_microphone("None")
        else:
            actions.speech.set_microphone(previous_mic)

        actions.speech.toggle()

    def microphone_preferred():
        """reverts to preferred microphone"""
        actions.speech.set_microphone(previous_mic)

    def speaker_selection_toggle():
        """"""
        if gui_speaker.showing:
            gui_speaker.hide()
        else:
            update_microphone_list()
            gui_speaker.show()

    def speaker_select(index: int):
        """Selects a speaker"""
        if 1 <= index and index <= len(speaker_device_list):
            device_name = speaker_device_list[index - 1]
            # print("selected thing: " + device_name)
            if app.platform == "mac":
                call(
                    [
                        "/usr/local/Cellar/switchaudio-osx/1.1.0/SwitchAudioSource",
                        "-t",
                        "output",
                        "-s",
                        device_name,
                    ]
                )
            elif app.platform == "windows":
                splits = device_name.split("(")
                device = splits[1].replace(")", "").strip()
                device_type = splits[0].strip()
                full_device_path = "{}\Device\\{}\\Render".format(device, device_type)
                program_files = os.environ["ProgramFiles"]
                call(
                    [
                        f"{program_files}/SoundVolumeView/SoundVolumeView.exe",
                        "/SetDefault",
                        full_device_path,
                        "0",
                    ]
                )

            app.notify("Activating speaker: {}".format(device_name))
            gui_speaker.hide()

    def system_switch_output_audio(name: str):
        """Switches output audio"""


def on_ready():
    ctx.register("devices_changed", devices_changed)
    update_microphone_list()
    actions.user.microphone_toggle()


app.register("ready", on_ready)
