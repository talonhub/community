from talon import actions
from talon import Module, actions, imgui, scripting, app
from talon.microphone import manager
from talon.lib import cubeb
from talon import scripting

ctx = cubeb.Context()
mod = Module()


def devices_changed(device_type):
    update_microphone_list()


microphone_device_list = []


def update_microphone_list():
    global microphone_device_list
    microphone_device_list = []
    for device in ctx.inputs():
        if str(device.state) == "DeviceState.ENABLED":
            microphone_device_list.append(device)


@imgui.open(software=app.platform == "linux")
def gui(gui: imgui.GUI):
    gui.text("Select a Microphone")
    gui.line()
    for index, item in enumerate(microphone_device_list, 1):
        if gui.button("{}. {}".format(index, item.name)):
            actions.user.microphone_select(index)


@mod.action_class
class Actions:
    def microphone_selection_toggle():
        """"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def microphone_select(index: int):
        """Selects a micropohone"""
        # print(str(index) + " " + str(len(microphone_device_list)))
        if 1 <= index and index <= len(microphone_device_list):
            microphone = microphone_device_list[index - 1].name
            for item in manager.menu.items:
                # print(item.name + " " + microphone)
                if microphone in item.name:
                    # manager.menu_click(item)
                    actions.speech.set_microphone(item.name)
                    app.notify("Activating {}".format(item.name))

                    break

            gui.hide()


ctx.register("devices_changed", devices_changed)


def on_launch():
    update_microphone_list()


app.register("launch", on_launch)

