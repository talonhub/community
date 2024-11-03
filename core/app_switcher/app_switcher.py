import os
import shlex
import subprocess
import time
from pathlib import Path

import talon
from talon import Context, Module, actions, app, fs, imgui, ui

# Construct a list of spoken form overrides for application names (similar to how homophone list is managed)
# These overrides are used *instead* of the generated spoken forms for the given app name or .exe (on Windows)
# CSV files contain lines of the form:
# <spoken form>,<app name or .exe> - to add a spoken form override for the app, or
# <app name or .exe> - to exclude the app from appearing in "running list" or "focus <app>"

# TODO: Consider moving overrides to settings directory
overrides_directory = os.path.dirname(os.path.realpath(__file__))
override_file_name = f"app_name_overrides.{talon.app.platform}.csv"
override_file_path = os.path.normcase(
    os.path.join(overrides_directory, override_file_name)
)

mod = Module()
mod.list("running", desc="all running applications")
mod.list("launch", desc="all launchable applications")
ctx = Context()

# a list of the current overrides
overrides = {}

# apps to exclude from running list
excludes = set()

# a list of the currently running application names
running_application_dict = {}


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

# on Windows, WindowsApps are not like normal applications, so
# we use the shell:AppsFolder to populate the list of applications
# rather than via e.g. the start menu. This way, all apps, including "modern" apps are
# launchable. To easily retrieve the apps this makes available, navigate to shell:AppsFolder in Explorer
if app.platform == "windows":
    import ctypes
    import os
    from ctypes import wintypes

    import pywintypes
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
        except OSError as e:
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
        yield from items_enum

    def list_known_folder(folder_id, htoken=None):
        result = []
        for item in enum_known_folder(folder_id, htoken):
            result.append(item.GetDisplayName(shellcon.SIGDN_NORMALDISPLAY))
        result.sort(key=lambda x: x.upper())
        return result

    def get_apps():
        items = {}
        for item in enum_known_folder(FOLDERID_AppsFolder):
            try:
                property_store = item.BindToHandler(
                    None, shell.BHID_PropertyStore, propsys.IID_IPropertyStore
                )
                app_user_model_id = property_store.GetValue(
                    pscon.PKEY_AppUserModel_ID
                ).ToString()

            except pywintypes.error:
                continue

            name = item.GetDisplayName(shellcon.SIGDN_NORMALDISPLAY)

            # exclude anything with install/uninstall...
            # 'cause I don't think we don't want 'em
            if "install" not in name.lower():
                items[name] = app_user_model_id

        return items

elif app.platform == "linux":
    import configparser
    import re

    linux_application_directories = [
        "/usr/share/applications",
        "/usr/local/share/applications",
        f"{Path.home()}/.local/share/applications",
        "/var/lib/flatpak/exports/share/applications",
        "/var/lib/snapd/desktop/applications",
    ]
    xdg_data_dirs = os.environ.get("XDG_DATA_DIRS")
    if xdg_data_dirs is not None:
        for directory in xdg_data_dirs.split(":"):
            linux_application_directories.append(f"{directory}/applications")
    linux_application_directories = list(set(linux_application_directories))

    def get_apps():
        # app shortcuts in program menu are contained in .desktop files. This function parses those files for the app name and command
        items = {}
        # find field codes in exec key with regex
        # https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html#exec-variables
        args_pattern = re.compile(r"\%[UufFcik]")
        for base in linux_application_directories:
            if os.path.isdir(base):
                for entry in os.scandir(base):
                    if entry.name.endswith(".desktop"):
                        try:
                            config = configparser.ConfigParser(interpolation=None)
                            config.read(entry.path)
                            # only parse shortcuts that are not hidden
                            if not config.has_option("Desktop Entry", "NoDisplay"):
                                name_key = config["Desktop Entry"]["Name"]
                                exec_key = config["Desktop Entry"]["Exec"]
                                # remove extra quotes from exec
                                if exec_key[0] == '"' and exec_key[-1] == '"':
                                    exec_key = re.sub('"', "", exec_key)
                                # remove field codes and add full path if necessary
                                if exec_key[0] == "/":
                                    items[name_key] = re.sub(args_pattern, "", exec_key)
                                else:
                                    exec_path = (
                                        subprocess.check_output(
                                            ["which", exec_key.split()[0]],
                                            stderr=subprocess.DEVNULL,
                                        )
                                        .decode("utf-8")
                                        .strip()
                                    )
                                    items[name_key] = (
                                        exec_path
                                        + " "
                                        + re.sub(
                                            args_pattern,
                                            "",
                                            " ".join(exec_key.split()[1:]),
                                        )
                                    )
                        except Exception:
                            print(
                                "linux get_apps(): skipped parsing application file ",
                                entry.name,
                            )
        return items

elif app.platform == "mac":
    mac_application_directories = [
        "/Applications",
        "/Applications/Utilities",
        "/System/Applications",
        "/System/Applications/Utilities",
        f"{Path.home()}/Applications",
        f"{Path.home()}/.nix-profile/Applications",
    ]

    def get_apps():
        items = {}
        for base in mac_application_directories:
            base = os.path.expanduser(base)
            if os.path.isdir(base):
                for name in os.listdir(base):
                    path = os.path.join(base, name)
                    name = name.rsplit(".", 1)[0].lower()
                    items[name] = path
        return items


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
    foreground_apps = ui.apps(background=False)

    for cur_app in foreground_apps:
        running_application_dict[cur_app.name.lower()] = cur_app.name

        if app.platform == "windows":
            exe = os.path.basename(cur_app.exe)
            running_application_dict[exe.lower()] = exe

    override_apps = excludes.union(overrides.values())

    running = actions.user.create_spoken_forms_from_list(
        [
            curr_app.name
            for curr_app in ui.apps(background=False)
            if curr_app.name.lower() not in override_apps
            and curr_app.exe.lower() not in override_apps
            and os.path.basename(curr_app.exe).lower() not in override_apps
        ],
        words_to_exclude=words_to_exclude,
        generate_subsequences=True,
    )

    for running_name, full_application_name in overrides.items():
        if running_app_name := running_application_dict.get(full_application_name):
            running[running_name] = running_app_name

    ctx.lists["self.running"] = running


def update_overrides(name, flags):
    """Updates the overrides and excludes lists"""
    global overrides, excludes

    if name is None or os.path.normcase(name) == override_file_path:
        overrides = {}
        excludes = set()

        # print("update_overrides")
        with open(override_file_path) as f:
            for line in f:
                line = line.rstrip().lower()
                line = line.split(",")
                if len(line) == 2 and line[0] != "Spoken form":
                    overrides[line[0]] = line[1].strip()
                if len(line) == 1:
                    excludes.add(line[0].strip())

        update_running_list()


@mod.action_class
class Actions:
    def get_running_app(name: str) -> ui.App:
        """Get the first available running app with `name`."""
        # We should use the capture result directly if it's already in the list
        # of running applications. Otherwise, name is from <user.text> and we
        # can be a bit fuzzier
        if name.lower() not in running_application_dict:
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
                and os.path.basename(application.exe).lower() == name
            ):
                return application
        raise RuntimeError(f'App not running: "{name}"')

    def switcher_focus(name: str):
        """Focus a new application by name"""
        app = actions.user.get_running_app(name)

        # Focus next window on same app
        if app == ui.active_app():
            actions.app.window_next()
        # Focus new app
        else:
            actions.user.switcher_focus_app(app)

    def switcher_focus_app(app: ui.App):
        """Focus application and wait until switch is made"""
        app.focus()
        t1 = time.perf_counter()
        while ui.active_app() != app:
            if time.perf_counter() - t1 > 1:
                raise RuntimeError(f"Can't focus app: {app.name}")
            actions.sleep(0.1)

    def switcher_focus_last():
        """Focus last window/application"""

    def switcher_focus_window(window: ui.Window):
        """Focus window and wait until switch is made"""
        window.focus()
        t1 = time.perf_counter()
        while ui.active_window() != window:
            if time.perf_counter() - t1 > 1:
                raise RuntimeError(f"Can't focus window: {window.title}")
            actions.sleep(0.1)

    def switcher_launch(path: str):
        """Launch a new application by path (all OSes), or AppUserModel_ID path on Windows"""
        if app.platform == "mac":
            ui.launch(path=path)
        elif app.platform == "linux":
            # Could potentially be merged with OSX code. Done in this explicit
            # way for expediency around the 0.4 release.
            cmd = shlex.split(path)[0]
            args = shlex.split(path)[1:]
            ui.launch(path=cmd, args=args)
        elif app.platform == "windows":
            is_valid_path = False
            try:
                current_path = Path(path)
                is_valid_path = current_path.is_file()
            except:
                is_valid_path = False
            if is_valid_path:
                ui.launch(path=path)
            else:
                cmd = f"explorer.exe shell:AppsFolder\\{path}"
                subprocess.Popen(cmd, shell=False)
        else:
            print("Unhandled platform in switcher_launch: " + app.platform)

    def switcher_menu():
        """Open a menu of running apps to switch to"""
        if app.platform == "windows":
            actions.key("alt-ctrl-tab")
        elif app.platform == "mac":
            # MacOS equivalent is "Mission Control"
            actions.user.dock_send_notification("com.apple.expose.awake")
        else:
            print("Persistent Switcher Menu not supported on " + app.platform)

    def switcher_toggle_running():
        """Shows/hides all running applications"""
        if gui_running.showing:
            gui_running.hide()
        else:
            gui_running.show()

    def switcher_hide_running():
        """Hides list of running applications"""
        gui_running.hide()


@imgui.open()
def gui_running(gui: imgui.GUI):
    gui.text("Running applications (with spoken forms)")
    gui.line()
    running_apps = sorted(
        (v.lower(), k, v) for k, v in ctx.lists["self.running"].items()
    )
    for _, running_name, full_application_name in running_apps:
        gui.text(f"{full_application_name}: {running_name}")

    gui.spacer()
    if gui.button("Running close"):
        actions.user.switcher_hide_running()


def update_launch_list():
    launch = get_apps()

    # actions.user.talon_pretty_print(launch)

    ctx.lists["self.launch"] = actions.user.create_spoken_forms_from_map(
        launch, words_to_exclude
    )


def ui_event(event, arg):
    if event in ("app_launch", "app_close"):
        update_running_list()


# Talon starts faster if you don't use the `talon.ui` module during launch


def on_ready():
    update_overrides(None, None)
    fs.watch(overrides_directory, update_overrides)
    update_launch_list()
    update_running_list()
    ui.register("", ui_event)


app.register("ready", on_ready)
