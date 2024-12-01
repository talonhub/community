import os
import shlex
import subprocess
import time
from pathlib import Path
import csv
import talon
from talon import Context, Module, actions, app, imgui, ui, resource
from typing import Union
from ..user_settings import track_csv_list

# Construct a list of spoken form overrides for application names (similar to how homophone list is managed)
# These overrides are used *instead* of the generated spoken forms for the given app name or .exe (on Windows)
# CSV files contain lines of the form:
# <spoken form>,<app name or .exe> - to add a spoken form override for the app, or
# <app name or .exe> - to exclude the app from appearing in "running list" or "focus <app>"

# TODO: Consider moving overrides to settings directory
directory = os.path.dirname(os.path.realpath(__file__))
app_names_file_name = f"app_names_{talon.app.platform}.csv"
app_names_file_path = os.path.normcase(
    os.path.join(directory, app_names_file_name)
)

mod = Module()
mod.list("running", desc="all running applications")
mod.list("launch", desc="all launchable applications")

ctx = Context()

# a list of the currently running application names
running_application_dict = {}

class Application:
    path: str
    display_name: str
    unique_identifier: str
    executable_name: str
    exclude: bool 
    spoken_forms: list[str]

    def __init__(self, path:str, display_name: str, unique_identifier: str, executable_name: str, exclude: bool, spoken_form: list[str]):
        self.path = path
        self.display_name = display_name
        self.executable_name = executable_name 
        self.unique_identifier = unique_identifier
        self.exclude = exclude
        self.spoken_forms = spoken_form  

    def __str__(self):
        spoken_form = None
        if self.spoken_forms:
            spoken_form = ";".join(self.spoken_forms)

        return f"{self.display_name},{spoken_form},{self.exclude},{self.unique_identifier},{self.path},{self.executable_name}"

# a dictionary of applications with overrides pre-applied
# key by app name, exe path, exe, and bundle id/AppUserModelId
applications = {}
known_application_list = []
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
got_apps = False
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
        
    def get_apps()-> list[Application]:
        global got_apps
        import win32com.client
        
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.NameSpace('shell:::{4234d49b-0245-4df3-b780-3893943456e1}')
        items = folder.Items()
        
        applications_dupe_prevention = {}
        for item in items:
            display_name = item.Name
            app_user_model_id = item.path
            path = None
            executable_name = None

            should_create_entry = "install" not in display_name

            if should_create_entry:
                p = resolve_path_with_guid(app_user_model_id)
                if p:
                    path = p.resolve()
                    executable_name = p.name  
                    # exclude anything that is NOT an actual executable
                    should_create_entry = p.suffix in [".exe"]

            new_app = Application(
                path=str(path) if path else None,
                display_name=display_name, 
                unique_identifier= app_user_model_id, 
                executable_name=executable_name if executable_name else None,
                exclude=False,
                spoken_form=None)
            
            if should_create_entry:
                if app_user_model_id not in applications_dupe_prevention:
                    known_application_list.append(new_app)
                    applications_dupe_prevention[app_user_model_id] = True
                else:
                    print(f"Potential duplicate app {new_app}")
        got_apps = True
        return known_application_list

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

    def get_apps() -> list[Application]:
        global applications
        from plistlib import load
        import glob
        applications_dupe_prevention = {}
        for base in mac_application_directories:
            base = os.path.expanduser(base)
            if os.path.isdir(base):
                for name in os.listdir(base):
                    new_app = None
                    path = os.path.join(base, name)
                    display_name = name.rsplit(".", 1)[0]
                    
                    # most, but not all, apps store this here
                    plist_path = os.path.join(path, "Contents/Info.plist")
                    
                    if os.path.exists(plist_path):
                        with open(plist_path, 'rb') as fp:
                            #print(f"found at default: {plist_path}")
                            pl = load(fp)
                            bundle_identifier = pl["CFBundleIdentifier"]
                            executable_name = pl["CFBundleExecutable"] if "CFBundleExecutable" in pl else None
                            use_alternate_name =  display_name.lower() == "utilities" and base in "/System/Applications/Utilities"
                            if use_alternate_name and not executable_name or bundle_identifier in applications_dupe_prevention:
                                continue                         

                            new_app = Application(
                                path=path,
                                display_name=display_name if not use_alternate_name else executable_name,
                                unique_identifier=bundle_identifier, 
                                executable_name=executable_name, 
                                exclude=False,
                                spoken_form=None)
                                                        
                            known_application_list.append(new_app)
                            applications_dupe_prevention[bundle_identifier] = True

                    else:
                        files = glob.glob(os.path.join(path, '**/Info.plist'), recursive=True)  

                        for file in files:
                            with open(file, 'rb') as fp:
                                pl = load(fp)
                                if "CFBundleIdentifier" in pl:
                                    #print(f"found at: {file}")
                                    bundle_identifier = pl["CFBundleIdentifier"]
                                    executable_name = pl["CFBundleExecutable"] if "CFBundleExecutable" in pl else None
                                    use_alternate_name =  display_name.lower() == "utilities" and base in "/System/Applications/Utilities"
                                    
                                    if use_alternate_name and not executable_name or bundle_identifier in applications_dupe_prevention:
                                        continue
                                       
                                    new_app = Application(
                                        path=path,
                                        display_name=display_name if not use_alternate_name else executable_name,   
                                        unique_identifier=bundle_identifier, 
                                        executable_name=executable_name, 
                                        exclude=False,
                                        spoken_form=None)
                                    
                                    known_application_list.append(new_app)
                                    applications_dupe_prevention[bundle_identifier] = True


        return known_application_list


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

def should_generate_spoken_forms(curr_app) -> tuple[bool, Union[Application, None]]:
    name = curr_app.name
    bundle_name = curr_app.bundle
    exe_path = str(Path(curr_app.exe).resolve())
    executable_name = os.path.basename(curr_app.exe)

    if bundle_name and bundle_name in applications_overrides:
        return not applications_overrides[bundle_name].exclude and applications_overrides[bundle_name].spoken_forms is None, applications_overrides[bundle_name]
    elif exe_path and exe_path in applications_overrides:
        return not applications_overrides[exe_path].exclude and applications_overrides[exe_path].spoken_forms is None, applications_overrides[exe_path]
    elif executable_name and executable_name in applications_overrides:
        value = not applications_overrides[executable_name].exclude and applications_overrides[executable_name].spoken_forms is None
        return value, applications_overrides[executable_name]    
    elif name and name in applications_overrides:
        return not applications_overrides[name].exclude and applications_overrides[name].spoken_forms is None, applications_overrides[name]
    return True, None

def update_running_list():
    global running_application_dict
    running_application_dict = {}
    running = {}
    foreground_apps = ui.apps(background=False)
    generate_spoken_form_list = []

    for cur_app in foreground_apps:
        name = cur_app.name.lower()
        running_application_dict[name.lower()] = cur_app
        
        if app.platform == "mac":
            bundle_name = cur_app.bundle.lower()
            running_application_dict[bundle_name] = cur_app

        if app.platform == "windows":
            exe = os.path.basename(cur_app.exe).lower()
            running_application_dict[cur_app.exe.lower()] = cur_app
            running_application_dict[exe] = cur_app

        should_generate_forms, override = should_generate_spoken_forms(cur_app)
        if should_generate_forms:
            generate_spoken_form_list.append(cur_app.name.lower())
        elif override and override.spoken_forms is not None:
            for spoken_form in override.spoken_forms:
                running[spoken_form] = name

        running.update(actions.user.create_spoken_forms_from_list(
            generate_spoken_form_list,
            words_to_exclude=words_to_exclude,
            generate_subsequences=True,
        ))

    ctx.lists["self.running"] = running

def write_default_csv():
    path = Path(app_names_file_path)
    if not path.exists():
        if not got_apps:
            get_apps()
        
        sorted_apps = sorted(known_application_list, key=lambda application: application.display_name)

        with open(path, 'w') as file:
            file.write("Application name, Spoken forms, Exclude, Unique Id, Path, Executable Name\n")
            
            for application in sorted_apps:
                file.write(str(application) + "\n")

write_default_csv()

@resource.watch(app_names_file_path)
def update(f):
    global applications, applications_overrides
    
    if not got_apps:
        get_apps()

    applications_overrides = {}
    rows = list(csv.reader(f))
    assert rows[0] == ["Application name", " Spoken forms", " Exclude"," Unique Id", " Path", " Executable Name"]

    for row in rows[1:]:
        if 0 == len(row):
            continue

        if len(row) != 6:
            print(f"Row {row} malformed; expecting 6 entires")

        display_name, spoken_forms, exclude, uid, path, executable_name = (
            [x.strip() or None for x in row])[:6]
        
        if spoken_forms.lower() == "none":
            spoken_forms = None
        else:
            spoken_forms = spoken_forms.split(";")
            
        exclude = False if exclude.lower() == "false" else True
        uid = None if uid.lower() == "none" else uid
        path = None if path.lower() == "none" else path
        executable_name = None if executable_name.lower() == "none" else executable_name
        override_app = Application (path=path,
                                    display_name=display_name, 
                                    unique_identifier=uid,
                                    executable_name=executable_name,
                                    exclude = exclude,
                                    spoken_form=spoken_forms,
                                    )
        
        # if display_name == "visual studio code":
        #     print("FOUND VISUAL STUDIO CODE!?!?")
        #     print(override_app)
            
        applications_overrides[override_app.display_name] = override_app

        if override_app.executable_name:
            applications_overrides[override_app.executable_name] = override_app

        if override_app.path:
            applications_overrides[override_app.path] = override_app                   

        if override_app.unique_identifier:
            applications_overrides[override_app.unique_identifier] = override_app

    # build the applications dictionary with the overrides applied
    applications = {}
    for application in known_application_list:
        curr_app = application

        if application.unique_identifier in applications_overrides:
            curr_app = applications_overrides[application.unique_identifier]

        if application.path in applications_overrides:
            curr_app = applications_overrides[application.path]

        if application.display_name in applications_overrides:
            curr_app = applications_overrides[application.display_name]
    
        if application.executable_name in applications_overrides:
            curr_app = applications_overrides[application.executable_name]
        
        #if curr_app.display_name == "visual studio code":
        #    print("found it agian?!?!")

        if curr_app.unique_identifier:
            applications[curr_app.unique_identifier] = curr_app

        if curr_app.path:
            applications[curr_app.path] = curr_app

        if curr_app.display_name:
            applications[curr_app.display_name] = curr_app
    
        if curr_app.executable_name:
            applications[curr_app.executable_name] = curr_app

    update_running_list()
    update_launch_list()


@mod.action_class
class Actions:
    def dump_apps_to_file():
        """what??"""
        sorted_apps = sorted(known_application_list, key=lambda application: application.display_name)

        with open("C:\\Users\\knaus\\app_names_windows.csv", 'w') as file:
            file.write("Application name, Spoken forms, Exclude, Unique Id, Path, Executable Name\n")
            
            for application in sorted_apps:
                file.write(str(application) + "\n")

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
        app = actions.user.get_running_app(name.lower())

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
            ui.launch(bundle=path)
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
    launch = {
        application.display_name : application.unique_identifier 
        for application in applications.values() 
        if not application.exclude and not application.spoken_forms
    }    

    result = actions.user.create_spoken_forms_from_map(
        sources=launch, 
        words_to_exclude=words_to_exclude,
        generate_subsequences=True,
    )

    customized = {
        spoken_form:  current_app.unique_identifier
        for current_app in applications.values()
        if current_app.spoken_forms is not None
        for spoken_form in current_app.spoken_forms
    }
    result.update(customized)
    ctx.lists["self.launch"] = result
