#todo
#(1) Consolidate logic for getting absolute paths of executables
#(2) Break out get_apps into action and move to operating system-specific area
#(3) Move CSVs to new style...
#(4) Simplify and consolidate logic for excludes
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

class Application:
    path: str
    display_name: str
    unique_identifier: str
    executable_name: str
    spoken_forms: list[str]
    exclude: bool 

    def __init__(self, path, display_name: str, unique_identifier: str, executable_name: str, exclude=False, spoken_forms: list[str] = None):
        self.path = path
        self.display_name = display_name
        self.executable_name = executable_name 
        self.unique_identifier = unique_identifier
        self.exclude = exclude

        self.spoken_forms = (
            [spoken_forms] if isinstance(spoken_forms, str) else spoken_forms
        )

applications = {}

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
    from .windows_known_paths import resolve_known_windows_path, PathNotFoundException
    from uuid import UUID

    def resolve_path_with_guid(path) -> Path:
        splits = path.split(os.path.sep)
        guid = splits[0]
        if is_valid_uuid(guid):
            try:
                known_folder_path = resolve_known_windows_path(UUID(guid))
            except (PathNotFoundException):
                print("Failed to resolve known path: " + guid)
                return None
            full_path = os.path.join(known_folder_path, *splits[1:])
            p = Path(full_path)
            return p
        return None

    def is_valid_uuid(value):
        try:
            uuid_obj = UUID(value, version=4)
            return True
        except ValueError:
            return False
        
    def get_apps()-> dict[str, Application]:
        import win32com.client
        
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.NameSpace('shell:::{4234d49b-0245-4df3-b780-3893943456e1}')
        items = folder.Items()
        
        for item in items:
            display_name = item.Name
            app_user_model_id = item.path
            path = None
            executable_name = None

            should_create_entry = "install" not in display_name.lower()

            if should_create_entry:
                p = resolve_path_with_guid(app_user_model_id)
                if p:
                    path = p.resolve()
                    executable_name = p.name  
                    # exclude anything that is NOT an actual executable
                    should_create_entry = p.suffix in [".exe"]

            if should_create_entry:
                should_exclude = display_name in excludes or app_user_model_id in excludes or path in excludes or executable_name in excludes

                if app_user_model_id not in applications:
                    new_app = Application(path, display_name, app_user_model_id, executable_name, should_exclude)

                    applications[app_user_model_id.lower()] = new_app

                    if new_app.path:
                        applications[str(new_app.path).lower()] = new_app
                    if executable_name:
                        applications[executable_name.lower()] = new_app
                    if display_name:
                        applications[display_name.lower()] = new_app

        return applications

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

    def get_apps() -> dict[str, Application]:
        global applications
        from plistlib import load
        import glob

        for base in mac_application_directories:
            base = os.path.expanduser(base)
            if os.path.isdir(base):
                for name in os.listdir(base):
                    path = os.path.join(base, name)
                    display_name = name.rsplit(".", 1)[0].lower() 
                    
                    # most, but not all, apps store this here
                    plist_path = os.path.join(path, "Contents/Info.plist")
                    
                    if os.path.exists(plist_path):
                        with open(plist_path, 'rb') as fp:
                            #print(f"found at default: {plist_path}")
                            pl = load(fp)
                            bundle_identifier = pl["CFBundleIdentifier"].lower()
                            executable_name = pl["CFBundleExecutable"] if "CFBundleExecutable" in pl else ""

                            # apply overrides
                            if bundle_identifier.lower() in overrides:
                                display_name = overrides[bundle_identifier].lower()
                            elif executable_name.lower() in overrides:
                                display_name = overrides[executable_name].lower()
                                
                            if bundle_identifier not in applications:
                                applications[bundle_identifier] = Application(path, display_name, bundle_identifier, executable_name)

                            applications[path] = Application(path, display_name, bundle_identifier, executable_name)
                    else:
                        files = glob.glob(os.path.join(path, '**/Info.plist'), recursive=True)  

                        for file in files:
                            with open(file, 'rb') as fp:
                                pl = load(fp)
                                if "CFBundleIdentifier" in pl:
                                    #print(f"found at: {file}")
                                    bundle_identifier = pl["CFBundleIdentifier"].lower()
                                    executable_name = pl["CFBundleExecutable"].lower() if "CFBundleExecutable" in pl else ""
                                    new_app = Application(path, display_name, bundle_identifier, executable_name)
                                    if bundle_identifier not in applications:
                                        applications[bundle_identifier.lower()] = new_app
                                        applications[path.lower()] = new_app
                                        applications[display_name.lower()] = new_app
                                        applications[executable_name.lower()] = new_app

        return applications


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

def should_add_running_app(curr_app):
    name = curr_app.name.lower()
    bundle_name = curr_app.bundle.lower()
    exe_path = str(Path(curr_app.exe).resolve()).lower() 
    executable_name = os.path.basename(curr_app.exe).lower()
    #print(name)
    if bundle_name and bundle_name in applications:
        return not applications[bundle_name].exclude and applications[bundle_name].spoken_forms is None
    elif exe_path and exe_path in applications:
        return not applications[exe_path].exclude and applications[exe_path].spoken_forms is None
    elif name and name in applications:
        return not applications[name].exclude and applications[name].spoken_forms is None
    elif executable_name and executable_name in applications:
        return not applications[executable_name].exclude and applications[executable_name].spoken_forms is None
    return True

def update_running_list():
    global running_application_dict
    running_application_dict = {}
    running = {}
    foreground_apps = ui.apps(background=False)

    for cur_app in foreground_apps:
        name = cur_app.name.lower()
        running_application_dict[name.lower()] = cur_app.name
        
        if app.platform == "mac":
            bundle_name = cur_app.bundle.lower()
            running_application_dict[bundle_name.lower()] = cur_app

        if app.platform == "windows":
            exe = os.path.basename(cur_app.exe).lower()
            running_application_dict[cur_app.exe.lower()] = cur_app
            running_application_dict[exe] = cur_app

        running = actions.user.create_spoken_forms_from_list(
            [
                cur_app.name
                for cur_app in ui.apps(background=False)
                if should_add_running_app(cur_app)
            ],
            words_to_exclude=words_to_exclude,
            generate_subsequences=False,
        )

    #print(overrides)
    for full_application_name, running_name in overrides.items():
        #print(f"{running_name} {full_application_name}")
        if full_application_name.lower() in running_application_dict:
            running[running_name] = full_application_name

    ctx.lists["self.running"] = running


def update_and_apply_overrides(name, flags):
    """Updates the overrides and excludes lists"""
    global overrides, excludes

    for key, cur_app in applications.items():
        cur_app.spoken_forms = None

    if name is None or os.path.normcase(name) == override_file_path:
        overrides = {}
        excludes = set()

        # print("update_and_apply_overrides")
        with open(override_file_path) as f:
            for line in f:
                line = line.rstrip().lower()
                line = line.split(",")
                if len(line) == 2 and line[0] != "Spoken form":
                    key = line[0].lower()
                    value = line[1].strip().lower()

                    if app.platform == "windows":
                        p = resolve_path_with_guid(line[0])
                        if p:
                            key = str(p.resolve()).lower()
                    overrides[key] = value

                    if key in applications:
                        current_app = applications[key]
                        if not current_app.spoken_forms:
                            current_app.spoken_forms = [value]
                        else:
                            current_app.spoken_forms.append(value)

                if len(line) == 1:
                    excludes.add(line[0].strip().lower())

        update_running_list()
        update_launch_list()


@mod.action_class
class Actions:
    def get_running_app(name: str) -> ui.App:
        """Get the first available running app with `name`."""
        # We should use the capture result directly if it's already in the list
        # of running applications. Otherwise, name is from <user.text> and we
        # can be a bit fuzzier
        if name.lower() in running_application_dict:
            return running_application_dict[name]
        
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
            if application.name == name or application.bundle.lower() == name or (
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
    if app.platform == "windows":
        launch = {app.display_name : app.unique_identifier for app in applications.values() if not app.exclude and not app.spoken_forms}    
    else:
        launch = {app.display_name : app.path  for app in applications.values() if not app.exclude and not app.spoken_forms}  

    result = actions.user.create_spoken_forms_from_map(
        launch, words_to_exclude
    )

    customized = {
        spoken_form:  current_app.unique_identifier
        for current_app in applications.values()
        if current_app.spoken_forms is not None
        for spoken_form in current_app.spoken_forms
    }

    result.update(customized)
    ctx.lists["self.launch"] = result

def ui_event(event, arg):
    if event in ("app_launch", "app_close"):
        update_running_list()

# Talon starts faster if you don't use the `talon.ui` module during launch


def on_ready():
    # build application dictionary
    get_apps()

    # get overrides first...
    update_and_apply_overrides(None, None)

    fs.watch(overrides_directory, update_and_apply_overrides)
    ui.register("", ui_event)


app.register("ready", on_ready)