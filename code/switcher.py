import os
import re
import time

from talon import Context, Module, app, imgui, ui, fs, actions

# Construct at startup a list of overides for application names (similar to how homophone list is managed)
# ie for a given talon recognition word set  `one note`, recognized this in these switcher functions as `ONENOTE`
# the list is a comma seperated `<Recognized Words>, <Overide>`
# TODO: Consider put list csv's (homophones.csv, app_name_overrides.csv) files together in a seperate directory,`knausj_talon/lists`
cwd = os.path.dirname(os.path.realpath(__file__))
overrides_directory = os.path.join(cwd, "app_names")
override_file_name = f"app_name_overrides.{app.platform}.csv"
override_file_path = os.path.join(overrides_directory, override_file_name)


mod = Module()
mod.list("running", desc="all running applications")
mod.list("launch", desc="all launchable applications")
ctx = Context()

# a list of the current overrides
overrides = {}

# a list of the currently running application names
running_application_dict = {}


@mod.capture
def running_applications(m) -> str:
    "Returns a single application name"


@mod.capture
def launch_applications(m) -> str:
    "Returns a single application name"


@ctx.capture(rule="{self.running}")  # | <user.text>)")
def running_applications(m):
    try:
        return m.running
    except AttributeError:
        return m.text


@ctx.capture(rule="{self.launch}")
def launch_applications(m):
    return m.launch


def split_camel(word):
    return re.findall(r"[0-9A-Z]*[a-z]+(?=[A-Z]|$)", word)


def get_words(name):
    words = re.findall(r"[0-9A-Za-z]+", name)
    out = []
    for word in words:
        out += split_camel(word)
    return out


def update_lists():
    global running_application_dict
    running_application_dict = {}
    running = {}
    for cur_app in ui.apps(background=False):
        name = cur_app.name

        if name.endswith(".exe"):
            name = name.rsplit(".", 1)[0]

        words = get_words(name)
        for word in words:
            if word and word not in running:
                running[word.lower()] = cur_app.name

        running[name.lower()] = cur_app.name
        running_application_dict[cur_app.name] = True

    for override in overrides:
        running[override] = overrides[override]

    ctx.lists["user.running"] = running


def update_overrides(name, flags):
    """Updates the overrides list"""
    global overrides
    overrides = {}

    if name is None or name == override_file_path:
        # print("update_overrides")
        with open(override_file_path, "r") as f:
            for line in f:
                line = line.rstrip()
                line = line.split(",")
                if len(line) == 2:
                    overrides[line[0].lower()] = line[1].strip()

        update_lists()


update_overrides(None, None)
fs.watch(overrides_directory, update_overrides)


@mod.action_class
class Actions:
    def get_running_app(name: str) -> ui.App:
        """Get the first available running app with `name`."""
        # We should use the capture result directly if it's already in the list
        # of running applications. Otherwise, name is from <user.text> and we
        # can be a bit fuzzier
        if name in running_application_dict:
            for app in ui.apps():
                if app.name == name and not app.background:
                    return app
            raise RuntimeError(f'App not running: "{name}"')
        else:
            # Don't process silly things like "focus i"
            if len(name) < 3:
                raise RuntimeError(
                    f'Skipped getting app: "{name}" has less than 3 chars.'
                )

            for running_name, app in ctx.lists["self.running"].items():
                if running_name == name or running_name.lower().startswith(
                    name.lower()
                ):
                    return app

            raise RuntimeError(f'Could not find app "{name}"')

    def switcher_focus(name: str):
        """Focus a new application by  name"""
        app = actions.self.get_running_app(name)
        app.focus()

        # Hacky solution to do this reliably on Mac.
        timeout = 5
        t1 = time.monotonic()
        # This line is producing an AttributeError for me on linux -rntz, 2020-10-04
        if app.platform == "mac":
            while ui.active_app() != app and time.monotonic() - t1 < timeout:
                time.sleep(0.1)

    def switcher_launch(path: str):
        """Launch a new application by path"""
        ui.launch(path=path)

    def switcher_toggle_running():
        """Shows/hides all running applications"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def switcher_hide_running():
        """Hides list of running applications"""
        gui.hide()


@imgui.open(software=False)
def gui(gui: imgui.GUI):
    gui.text("Names of running applications")
    gui.line()
    for line in ctx.lists["self.running"]:
        gui.text(line)


def update_launch_list():
    if app.platform == "mac":
        launch = {}
        for base in (
            "/Applications",
            "/Applications/Utilities",
            "/System/Applications",
            "/System/Applications/Utilities",
        ):
            if os.path.isdir(base):
                for name in os.listdir(base):
                    # print(name)
                    path = os.path.join(base, name)
                    name = name.rsplit(".", 1)[0].lower()
                    launch[name] = path
                    words = name.split(" ")
                    for word in words:
                        if word and word not in launch:
                            if len(name) > 6 and len(word) < 3:
                                continue

                            launch[word] = path

        ctx.lists["user.launch"] = launch


def ui_event(event, arg):
    if event in ("app_launch", "app_close"):
        update_lists()

# Currently update_launch_list only does anything on mac, so we should make sure
# to initialize user launch to avoid getting "List not found: user.launch"
# errors on other platforms.
ctx.lists["user.launch"] = {}
update_launch_list()
ui.register("", ui_event)

