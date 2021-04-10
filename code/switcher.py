import csv
import os
import re
import shutil
import time
from glob import glob
from itertools import islice
from pathlib import Path

import talon
from talon import Context, Module, actions, app, imgui, resource, ui

from .user_settings import get_list_from_csv

override_file_name = f"app_name_overrides.{talon.app.platform}.csv"

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
    "and",
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
    "microsoft",
    "windows",
    "Windows",
]

# windows-specific logic
if app.platform == "windows":
    import ctypes
    import os

    import pythoncom
    import pywintypes
    import winerror

    try:
        import winreg
    except ImportError:
        # Python 2
        import _winreg as winreg

        bytes = lambda x: str(buffer(x))

    from ctypes import wintypes

    from win32com.propsys import propsys, pscon
    from win32com.shell import shell, shellcon

    # KNOWNFOLDERID
    # https://msdn.microsoft.com/en-us/library/dd378457
    # win32com defines most of these, except the ones added in Windows 8.
    FOLDERID_AppsFolder = pywintypes.IID("{1e87508d-89c2-42f0-8a7e-645a0f50ca58}")

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
            _shell32.SHGetKnownFolderIDList(folder_id, 0, htoken, ctypes.byref(pidl))
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


def split_camel(word):
    return re.findall(r"[0-9A-Z]*[a-z]+(?=[A-Z]|$)", word)


def get_words(name):
    words = re.findall(r"[0-9A-Za-z]+", name)
    out = []
    for word in words:
        out += split_camel(word)
    return out


def update_running_list():
    global running_application_dict
    running_application_dict = {}
    running = {}
    for cur_app in ui.apps(background=False):
        name = cur_app.name

        if name.endswith(".exe"):
            name = name.rsplit(".", 1)[0]

        words = get_words(name)
        for word in words:
            if word and word not in running and len(word) >= 3:
                running[word.lower()] = cur_app.name

        running[name.lower()] = cur_app.name
        running_application_dict[cur_app.name] = True

    for override in overrides:
        running[override] = overrides[override]

    lists = {
        "self.running": running,
    }

    # batch update lists
    ctx.lists.update(lists)


pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d|[+]")

# todo: this is garbage
def create_spoken_forms(name, max_len=30):
    result = " ".join(list(islice(pattern.findall(name), max_len)))

    result = (
        result.replace("0", "zero")
        .replace("1", "one")
        .replace("2", "two")
        .replace("3", "three")
        .replace("4", "four")
        .replace("5", "five")
        .replace("6", "six")
        .replace("7", "seven")
        .replace("8", "eight")
        .replace("9", "nine")
        .replace("+", "plus")
    )
    return result


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
        for app in ui.apps():
            if app.name == name and not app.background:
                return app
        raise RuntimeError(f'App not running: "{name}"')

    def switcher_focus(name: str):
        """Focus a new application by  name"""
        app = actions.user.get_running_app(name)
        app.focus()

        # Hacky solution to do this reliably on Mac.
        timeout = 5
        t1 = time.monotonic()
        if talon.app.platform == "mac":
            while ui.active_app() != app and time.monotonic() - t1 < timeout:
                time.sleep(0.1)

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
                    words = name.split(" ")
                    for word in words:
                        if word and word not in launch:
                            if len(name) > 6 and len(word) < 3:
                                continue
                            launch[word] = path

    elif app.platform == "windows":
        shortcuts = enum_known_folder(FOLDERID_AppsFolder)
        # str(shortcuts)
        for name in shortcuts:
            # print("hit: " + name)
            # print(name)
            # name = path.rsplit("\\")[-1].split(".")[0].lower()
            if "install" not in name:
                spoken_form = create_spoken_forms(name)
                # print(spoken_form)
                launch[spoken_form] = name
                words = spoken_form.split(" ")
                for word in words:
                    if word not in words_to_exclude and word not in launch:
                        if len(name) > 6 and len(word) < 3:
                            continue
                        launch[word] = name

    ctx.lists["self.launch"] = launch


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
    update_launch_list()
    update_running_list()
    ui.register("", ui_event)


# construct the legacy path name. todo: remove in Talon v0.2 timeframe
cwd = os.path.dirname(os.path.realpath(__file__))
legacy_path = Path(os.path.join(cwd, "app_names", override_file_name))

overrides = get_list_from_csv(
    override_file_name,
    headers=None,
    spoken_form_first=True,
    strip_whitepsace_from_output=True,
    legacy_path=legacy_path,
)

app.register("ready", on_ready)
