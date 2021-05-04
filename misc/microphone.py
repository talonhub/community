# From https://github.com/nriley/knausj_talon/blob/061e0d48b221a144164327d7f2854cbb7a7dbd8a/misc/microphone.py
from talon import actions, noise, registry
from talon.microphone import manager

PREFERRED_MICROPHONES = ("Yeti Stereo Microphone", "Scarlett Solo USB")


def device_name(device):
    name = device.name
    # Windows microphone device names are of the format "Microphone (...)"
    if name.startswith("Microphone (") and name.endswith(")"):
        name = name[12:-1]
    return name


def mic_changed_to(device):
    if device and device_name(device) not in PREFERRED_MICROPHONES:
        actions.speech.set_microphone("None")


manager.register("mic_change", mic_changed_to)

# note: cubeb API may not be stable; don't rely on this
from talon.lib import cubeb

ctx = cubeb.Context()


def devices_changed(device_type):
    if device_type is cubeb.DeviceType.INPUT:
        for device in ctx.inputs():
            if device.state is not cubeb.DeviceState.ENABLED:
                continue
            name = device_name(device)
            if name in PREFERRED_MICROPHONES:
                print(f"Setting microphone to {name}")
                actions.speech.set_microphone(device.name)
                # actions.speech.enable()
                app.notify(f"Microphone set to '{name}'")
                return
        print(f"Setting microphone to None")
        actions.speech.set_microphone("None")
        app.notify("Microphone set to None")


ctx.register("devices_changed", devices_changed)

# at startup, disable speech recognition if no preferred microphone connected
from talon import app

app.register("launch", lambda: devices_changed(cubeb.DeviceType.INPUT))
