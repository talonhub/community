import os
import re
import time

import talon

from talon import Context, Module, app, imgui, ui, fs, actions
from glob import glob
from itertools import islice
from pathlib import Path

# Construct at startup a list of overides for application names (similar to how homophone list is managed)
# ie for a given talon recognition word set  `one note`, recognized this in these switcher functions as `ONENOTE`
# the list is a comma seperated `<Recognized Words>, <Overide>`
# TODO: Consider put list csv's (homophones.csv, app_name_overrides.csv) files together in a seperate directory,`knausj_talon/lists`
cwd = os.path.dirname(os.path.realpath(__file__))
overrides_directory = os.path.join(cwd, "app_names")
override_file_name = f"app_name_overrides.{talon.app.platform}.csv"
override_file_path = os.path.join(overrides_directory, override_file_name)

mod = Module()
mod.list("running", desc="all running applications")
mod.list("launch", desc="all launchable applications")
ctx = Context()

# a list of the current overrides
overrides = {}

# a list of the currently running application names
running_application_dict = {}


mac_application_directories = [
    "/Applications",
    "/Applications/Utilities",
    "/System/Applications",
    "/System/Applications/Utilities",
]

# windows_application_directories = [
#     "%AppData%/Microsoft/Windows/Start Menu/Programs",
#     "%ProgramData%/Microsoft/Windows/Start Menu/Programs",
#     "%AppData%/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar",
# ]

words_to_exclude = [
    "zero",
    "one",
    "two",
    "three",
    "for",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "and",
    "dot",
    "exe",
    "help",
    "install",
    "installer",
    "microsoft",
    "nine",
    "readme",
    "studio",
    "terminal",
    "visual",
    "windows",
]

# windows-specific logic
if app.platform == "windows":
    import os
    import ctypes
    import pywintypes
    import pythoncom
    import winerror

    try:
        import winreg
    except ImportError:
        # Python 2
        import _winreg as winreg

        def bytes(x): return str(buffer(x))

    from ctypes import wintypes
    from win32com.shell import shell, shellcon
    from win32com.propsys import propsys, pscon

    # KNOWNFOLDERID
    # https://msdn.microsoft.com/en-us/library/dd378457
    # win32com defines most of these, except the ones added in Windows 8.
    FOLDERID_AppsFolder = pywintypes.IID(
        "{1e87508d-89c2-42f0-8a7e-645a0f50ca58}")

    # win32com is missing SHGetKnownFolderIDList, so use ctypes.

    _ole32 = ctypes.OleDLL("ole32")
    _shell32 = ctypes.OleDLL("shell32")

    _REFKNOWNFOLDERID = ctypes.c_char_p
    _PPITEMIDLIST = ctypes.POINTER(ctypes.c_void_p)

    _ole32.CoTaskMemFree.restype = None
    _ole32.CoTaskMemFree.argtypes = (wintypes.LPVOID,)

    _shell32.SHGetKnownFolderIDList.argtypes = (
        _REFKNOWNFOLDERID,  # rfid
        wintypes.DWORD,  # dwFlags
        wintypes.HANDLE,  # hToken
        _PPITEMIDLIST,
    )  # ppidl

    def get_known_folder_id_list(folder_id, htoken=None):
        if isinstance(folder_id, pywintypes.IIDType):
            folder_id = bytes(folder_id)
        pidl = ctypes.c_void_p()
        try:
            _shell32.SHGetKnownFolderIDList(
                folder_id, 0, htoken, ctypes.byref(pidl))
            return shell.AddressAsPIDL(pidl.value)
        except WindowsError as e:
            if e.winerror & 0x80070000 == 0x80070000:
                # It's a WinAPI error, so re-raise it, letting Python
                # raise a specific exception such as FileNotFoundError.
                raise ctypes.WinError(e.winerror & 0x0000FFFF)
            raise
        finally:
            if pidl:
                _ole32.CoTaskMemFree(pidl)

    def enum_known_folder(folder_id, htoken=None):
        id_list = get_known_folder_id_list(folder_id, htoken)
        folder_shell_item = shell.SHCreateShellItem(None, None, id_list)
        items_enum = folder_shell_item.BindToHandler(
            None, shell.BHID_EnumItems, shell.IID_IEnumShellItems
        )
        result = []
        for item in items_enum:
            # print(item.GetDisplayName(shellcon.SIGDN_NORMALDISPLAY))
            result.append(item.GetDisplayName(shellcon.SIGDN_NORMALDISPLAY))

        return result

    def list_known_folder(folder_id, htoken=None):
        result = []
        for item in enum_known_folder(folder_id, htoken):
            result.append(item.GetDisplayName(shellcon.SIGDN_NORMALDISPLAY))
        result.sort(key=lambda x: x.upper())
        return result


@mod.capture(rule="{self.running}")  # | <user.text>)")
def running_applications(m) -> str:
    "Returns a single application name"
    try:
        return m.running
    except AttributeError:
        return m.text


@mod.capture(rule="{self.launch}")
def launch_applications(m) -> str:
    "Returns a single application name"
    return m.launch


def update_running_list():
    global running_application_dict
    running_application_dict = {}
    running = {}
    for cur_app in ui.apps(background=False):
        running_application_dict[cur_app.name] = True

        if app.platform == "windows":
            # print("hit....")
            # print(cur_app.exe)
            running_application_dict[cur_app.exe.split(os.path.sep)[-1]] = True

    running = actions.user.create_spoken_forms_from_list(
        [curr_app.name for curr_app in ui.apps(background=False)],
        words_to_exclude=words_to_exclude,
        generate_subsequences=True,
    )

    # print(str(running_application_dict))
    # todo: should the overrides remove the other spoken forms for an application?
    for override in overrides:
        if overrides[override] in running_application_dict:
            running[override] = overrides[override]

    lists = {
        "self.running": running,
        # "self.launch": launch,
    }

    # batch update lists
    ctx.lists.update(lists)


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

        update_running_list()

@mod.action_class
class Actions:
    def get_running_app(name: str) -> ui.App:
        """Get the first available running app with `name`."""
        # We should use the capture result directly if it's already in the list
        # of running applications. Otherwise, name is from <user.text> and we
        # can be a bit fuzzier
        if name not in running_application_dict:
            if len(name) < 3:
                raise RuntimeError(
                    f'Skipped getting app: "{name}" has less than 3 chars.'
                )
            for running_name, full_application_name in ctx.lists[
                "self.running"
            ].items():
                if running_name == name or running_name.lower().startswith(
                    name.lower()
                ):
                    name = full_application_name
                    break
        for application in ui.apps(background=False):
            if application.name == name or (
                app.platform == "windows"
                and application.exe.split(os.path.sep)[-1] == name
            ):
                return application
        raise RuntimeError(f'App not running: "{name}"')

    def switcher_focus(name: str):
        """Focus a new application by name"""
        app = actions.user.get_running_app(name)
        actions.user.switcher_focus_app(app)

    def switcher_focus_app(app: ui.App):
        """Focus application and wait until switch is made"""
        app.focus()
        t1 = time.monotonic()
        while ui.active_app() != app:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus app: {app.name}")
            actions.sleep(0.1)

    def switcher_focus_window(window: ui.Window):
        """Focus window and wait until switch is made"""
        window.focus()
        t1 = time.monotonic()
        while ui.active_window() != window:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus window: {window.title}")
            actions.sleep(0.1)

    def switcher_launch(path: str):
        """Launch a new application by path"""
        if app.platform == "windows":
            is_valid_path = False
            try:
                current_path = Path(path)
                is_valid_path = current_path.is_file()
                # print("valid path: {}".format(is_valid_path))

            except:
                # print("invalid path")
                is_valid_path = False

            if is_valid_path:
                # print("path: " + path)
                ui.launch(path=path)

            else:
                # print("envelop")
                actions.key("super-s")
                actions.sleep("300ms")
                actions.insert("apps: {}".format(path))
                actions.sleep("150ms")
                actions.key("enter")

        else:
            ui.launch(path=path)

    def switcher_menu():
        """Open a menu of running apps to switch to"""
        if app.platform == "windows":
            actions.key("alt-ctrl-tab")
        else:
            print("Persistent Switcher Menu not supported on " + app.platform)

    def switcher_toggle_running():
        """Shows/hides all running applications"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def switcher_hide_running():
        """Hides list of running applications"""
        gui.hide()


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Names of running applications")
    gui.line()
    for line in ctx.lists["self.running"]:
        gui.text(line)


def update_launch_list():
    launch = {}
    if app.platform == "mac":
        for base in mac_application_directories:
            if os.path.isdir(base):
                for name in os.listdir(base):
                    path = os.path.join(base, name)
                    name = name.rsplit(".", 1)[0].lower()
                    launch[name] = path

    elif app.platform == "windows":
        shortcuts = enum_known_folder(FOLDERID_AppsFolder)
        shortcuts.sort()
        for name in shortcuts:
            # print("hit: " + name)
            # print(name)
            # name = path.rsplit("\\")[-1].split(".")[0].lower()
            if "install" not in name:
                launch[name] = name

    ctx.lists["self.launch"] = actions.user.create_spoken_forms_from_map(
        launch, words_to_exclude
    )


def ui_event(event, arg):
    if event in ("app_launch", "app_close"):
        update_running_list()


# Currently update_launch_list only does anything on mac, so we should make sure
# to initialize user launch to avoid getting "List not found: user.launch"
# errors on other platforms.
ctx.lists["user.launch"] = {}
ctx.lists["user.running"] = {}

# Talon starts faster if you don't use the `talon.ui` module during launch


def on_ready():
    update_overrides(None, None)
    fs.watch(overrides_directory, update_overrides)
    update_launch_list()
    update_running_list()
    ui.register("", ui_event)
app.register("ready", on_ready)
