import os
import shlex
import subprocess
import time
from pathlib import Path
import csv
import talon
from talon import Context, Module, actions, app, imgui, ui, resource
from .windows import get_installed_windows_apps
from .mac import get_installed_mac_apps
from typing import Union
from .application import Application
import re

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

# a dictionary of applications with overrides pre-applied
# key by app name, exe path, exe, and bundle id/AppUserModelId
applications = {}

INSTALLED_APPLICATIONS_LIST: list[Application] = []

# list of applications that appear in the CSV, but do not appear to be installed
# these are preserved when the csv is re-written
PRESERVED_APPLICATION_LIST: list[Application] = []
INSTALLED_APPLICATIONS_INITIALIZED = False

# Define the regex pattern for a bundle ID
bundle_id_pattern = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$'

# Compile the regex pattern
compiled_pattern = re.compile(bundle_id_pattern)

# Function to check if a string is a bundle ID
def is_bundle_id(string):
    return bool(compiled_pattern.match(string))

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

def should_generate_spoken_forms_for_running_app(curr_app) -> tuple[bool, Union[Application, None]]:
    name = curr_app.name
    bundle_name = curr_app.bundle
    exe_path = str(Path(curr_app.exe).resolve())
    executable_name = os.path.basename(curr_app.exe)

    # we do not exclude these apps from the running list in case they're started thru other means

    if bundle_name and bundle_name in APPLICATIONS_OVERRIDES:
        #return not APPLICATIONS_OVERRIDES[bundle_name].exclude and APPLICATIONS_OVERRIDES[bundle_name].spoken_forms is None, APPLICATIONS_OVERRIDES[bundle_name]
        return APPLICATIONS_OVERRIDES[bundle_name].spoken_forms is None, APPLICATIONS_OVERRIDES[bundle_name]
    elif exe_path and exe_path in APPLICATIONS_OVERRIDES:
        #return not APPLICATIONS_OVERRIDES[exe_path].exclude and APPLICATIONS_OVERRIDES[exe_path].spoken_forms is None, APPLICATIONS_OVERRIDES[exe_path]
        return APPLICATIONS_OVERRIDES[exe_path].spoken_forms is None, APPLICATIONS_OVERRIDES[exe_path]
    elif executable_name and executable_name in APPLICATIONS_OVERRIDES:
        #return not APPLICATIONS_OVERRIDES[executable_name].exclude and APPLICATIONS_OVERRIDES[executable_name].spoken_forms is None, APPLICATIONS_OVERRIDES[executable_name]  
        return APPLICATIONS_OVERRIDES[executable_name].spoken_forms is None, APPLICATIONS_OVERRIDES[executable_name]      
    elif name and name in APPLICATIONS_OVERRIDES:
        return APPLICATIONS_OVERRIDES[name].spoken_forms is None, APPLICATIONS_OVERRIDES[name]
        #return not APPLICATIONS_OVERRIDES[name].exclude and APPLICATIONS_OVERRIDES[name].spoken_forms is None, APPLICATIONS_OVERRIDES[name]
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

        should_generate_forms, override = should_generate_spoken_forms_for_running_app(cur_app)
        if should_generate_forms:
            generate_spoken_form_list.append(cur_app.name.lower())
        elif override and override.spoken_forms is not None:
            for spoken_form in override.spoken_forms:
                running[spoken_form] = name

        running.update(actions.user.create_spoken_forms_from_list(
            generate_spoken_form_list,
            words_to_exclude=words_to_exclude,
            generate_subsequences=False,
        ))

    ctx.lists["self.running"] = running

def get_installed_apps():
    global INSTALLED_APPLICATIONS_LIST, INSTALLED_APPLICATIONS_INITIALIZED
    if not INSTALLED_APPLICATIONS_INITIALIZED:
        if app.platform == "windows":
            INSTALLED_APPLICATIONS_LIST = get_installed_windows_apps()
        elif app.platform == "mac":
            INSTALLED_APPLICATIONS_LIST = get_installed_mac_apps()
        INSTALLED_APPLICATIONS_INITIALIZED = True

def update_csv(forced: bool = False):
    path = Path(app_names_file_path)
    get_installed_apps()

    if not path.exists() or forced:
        all_apps = [*INSTALLED_APPLICATIONS_LIST, *PRESERVED_APPLICATION_LIST]

        sorted_apps = sorted(all_apps, key=lambda application: application.display_name)

        output = ["Application name, Spoken forms, Exclude, Unique Id, Path, Executable Name\n"]
        for application in sorted_apps:
            output.extend(f"{str(application)}\n") 

        with open(path, 'w') as file:
            file.write("".join(output))

update_csv()

@resource.watch(app_names_file_path)
def update(f):
    global applications, INSTALLED_APPLICATIONS_LIST, APPLICATIONS_OVERRIDES, INSTALLED_APPLICATIONS_INITIALIZED
    global PRESERVED_APPLICATION_LIST
    
    get_installed_apps()

    application_map = {
        app.unique_identifier : app for app in INSTALLED_APPLICATIONS_LIST
    }

    APPLICATIONS_OVERRIDES = {}
    PRESERVED_APPLICATION_LIST = []
    removed_apps_dict = {}

    must_update_file = False

    rows = list(csv.reader(f))
    assert rows[0] == ["Application name", " Spoken forms", " Exclude"," Unique Id", " Path", " Executable Name"]
    if len(rows[1:]) < len(INSTALLED_APPLICATIONS_LIST):
        must_update_file = True
    
    for row in rows[1:]:
        if len(row) != 6:
            print(f"Row {row} malformed; expecting 6 entires")

        display_name, spoken_forms, exclude, uid, path, executable_name = (
            [x.strip() or None for x in row])[:6]
        
        if spoken_forms.lower() == "none":
            spoken_forms = None
        else:
            spoken_forms = [spoken_form.strip() for spoken_form in spoken_forms.split(";")]
            
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
        
        # app has been removed from the OS or is not installed yet.
        # lets preserve this entry for the convenience
        if uid not in application_map and uid not in removed_apps_dict:
            removed_apps_dict[uid] = True
            PRESERVED_APPLICATION_LIST.append(override_app)
    
        APPLICATIONS_OVERRIDES[override_app.display_name] = override_app

        if override_app.executable_name:
            APPLICATIONS_OVERRIDES[override_app.executable_name] = override_app

        if override_app.path:
            APPLICATIONS_OVERRIDES[override_app.path] = override_app                   

        if override_app.unique_identifier:
            APPLICATIONS_OVERRIDES[override_app.unique_identifier] = override_app

    # build the applications dictionary with the overrides applied
    applications = {}
    for index,application in enumerate(INSTALLED_APPLICATIONS_LIST):
        curr_app = application

        if application.unique_identifier in APPLICATIONS_OVERRIDES:
            curr_app = APPLICATIONS_OVERRIDES[application.unique_identifier]
            INSTALLED_APPLICATIONS_LIST[index] = curr_app
        else:
             must_update_file = True

        if curr_app.unique_identifier:
            applications[curr_app.unique_identifier] = curr_app

        if curr_app.path:
            applications[curr_app.path] = curr_app

        if curr_app.display_name:
            applications[curr_app.display_name] = curr_app
    
        if curr_app.executable_name:
            applications[curr_app.executable_name] = curr_app

    if must_update_file:
        print(f"Missing or new application detected, updating {app_names_file_name}")
        update_csv(True)
    else:
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
            if is_bundle_id(path):
                ui.launch(bundle=path)
            else: 
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
    launch = {
        application.display_name : application.unique_identifier 
        for application in applications.values() 
        if not application.exclude and not application.spoken_forms
    }    

    result = actions.user.create_spoken_forms_from_map(
        sources=launch, 
        words_to_exclude=words_to_exclude,
        generate_subsequences=False,
    )

    customized = {
        spoken_form:  current_app.unique_identifier
        for current_app in applications.values()
        if current_app.spoken_forms is not None
        for spoken_form in current_app.spoken_forms
    }
    result.update(customized)
    ctx.lists["self.launch"] = result
