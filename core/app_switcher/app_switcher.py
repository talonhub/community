import os
import shlex
import subprocess
import time
from pathlib import Path
import csv
import talon
from talon import Context, Module, actions, app, imgui, ui, resource
from .windows import get_installed_windows_apps, application_frame_host_path, application_frame_host, application_frame_host_group, get_application_user_model_id, get_application_user_model_for_window
from .windows_applications import get_known_windows_application
from .mac import get_installed_mac_apps
from .exclusion import ExclusionType, RunningApplicationExclusion
from typing import Union
from .application import Application, ApplicationGroup
import re
from talon.ui import Rect
from talon.windows.ax import Element
from dataclasses import dataclass

import platform
hostname = platform.node()
base_script_directory = os.path.dirname(os.path.realpath(__file__))
csv_directory = os.path.join(base_script_directory, talon.app.platform, hostname)
running_applications_exclusions_filename = "running_applications_exclusions.csv"
running_applications_file_path = os.path.normcase(
    os.path.join(csv_directory, running_applications_exclusions_filename)
)

launch_applications_filename = "launch_applications.csv"
launch_applications_file_path = os.path.normcase(
    os.path.join(csv_directory, launch_applications_filename)
)

if not os.path.exists(csv_directory):
    # Create the directory
    os.makedirs(csv_directory)

mod = Module()
mod.tag("app_switcher_selector_showing", desc="Indicates the app_switcher_selector_showing")
mod.list("running", desc="all running applications")
mod.list("launch", desc="all launchable applications")
mod.list("running_applications", desc="all running applications")

ctx = Context()

# a list of the currently running application names
RUNNING_APPLICATION_DICT = {}

# exclusions applied to the running applications list (user.running)
# key is exe, path, bundle, etc
RUNNING_APPLICATION_EXCLUSIONS_DICT = {}

# list of all application exclusions
RUNNING_APPLICATION_EXCLUSIONS = []

# a dictionary of applications with overrides pre-applied
# key by app name, exe path, exe, and bundle id/AppUserModelId
APPLICATIONS_DICT = {}

# list of known, installed applications
INSTALLED_APPLICATIONS_LIST: list[Application] = []

# list of application groups. mapped by executable path or name
APPLICATION_GROUPS_DICT = {}

# dictionary of application overrides from launch file
APPLICATIONS_OVERRIDES = {}

WINDOWS_NAME_TO_TALON_NAME = {}

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

def get_override_by_app_user_model_id(uuid, curr_app):
    if uuid.lower() in APPLICATIONS_OVERRIDES:
        return APPLICATIONS_OVERRIDES[uuid.lower()]
    
    return get_override_for_running_app(curr_app)

def get_override_for_running_app(curr_app) -> Union[Application | ApplicationGroup | RunningApplicationExclusion | None]:
    name = curr_app.name
    bundle_name = curr_app.bundle
    exe_path = str(Path(curr_app.exe).resolve()).lower()
    executable_name = os.path.basename(curr_app.exe).lower()

    # if app.platform == "windows":
    #     override = get_windows_application_override(executable_name)
    #     if override:
    #         print(f"windows application override found {executable_name}")
    #         return override
    if exe_path in RUNNING_APPLICATION_EXCLUSIONS_DICT:
        return RUNNING_APPLICATION_EXCLUSIONS_DICT[exe_path]
    elif executable_name in RUNNING_APPLICATION_EXCLUSIONS_DICT:
        return RUNNING_APPLICATION_EXCLUSIONS_DICT[executable_name]
    elif bundle_name in RUNNING_APPLICATION_EXCLUSIONS_DICT:
        return RUNNING_APPLICATION_EXCLUSIONS_DICT[bundle_name]
    elif name in RUNNING_APPLICATION_EXCLUSIONS_DICT:
        return RUNNING_APPLICATION_EXCLUSIONS_DICT[name]

    # application groups take precedence
    if exe_path in APPLICATION_GROUPS_DICT:
        return APPLICATION_GROUPS_DICT[exe_path]
    elif executable_name in APPLICATION_GROUPS_DICT:
        return APPLICATION_GROUPS_DICT[executable_name]
    
    # otherwise, check for application overrides
    if bundle_name and bundle_name in APPLICATIONS_OVERRIDES:
        override = APPLICATIONS_OVERRIDES[bundle_name]
        return override
    elif exe_path and exe_path in APPLICATIONS_OVERRIDES:
        override = APPLICATIONS_OVERRIDES[exe_path]
        return override
    elif executable_name and executable_name in APPLICATIONS_OVERRIDES:
        override = APPLICATIONS_OVERRIDES[executable_name]
        return override 
    elif name and name in APPLICATIONS_OVERRIDES:
        override = APPLICATIONS_OVERRIDES[name]
        return override 

    # if we made it here, no overrides found
    return None

app_frame_host_cache = {}

pending_app = None
valid_windows_for_pending_app = None

@imgui.open()
def gui_switcher_chooser(gui: imgui.GUI):
    # if no selected context, draw the contexts
    for index, window in enumerate(valid_windows_for_pending_app, 1):
        button_name = f"{index}. {window.title}"

        if gui.button(button_name):
            window.focus()
            gui_switcher_chooser.hide()
            ctx.tags = []


def is_window_valid(window: ui.Window) -> bool:
    """Returns true if this window is valid for focusing"""
    return (
        not window.hidden
        # On Windows, there are many fake windows with empty titles -- this excludes them.
        and len(window.title) > 0
        and "chrome legacy window" not in window.title.lower()
        # This excludes many tiny windows that are not actual windows, and is a rough heuristic.
        and window.rect.width > window.screen.dpi
        and window.rect.height > window.screen.dpi
    )


def get_valid_windows(app: ui.App):
    valid_windows = []
    for window in app.windows():
        if is_window_valid(window):
            valid_windows.append(window)

    return valid_windows

def get_valid_windows_by_app_user_model_id(app: ui.App) -> dict[str, list]:
    valid_windows = {}
    
    for window in app.windows():
        if is_window_valid(window):
            window_app_user_model_id = get_application_user_model_for_window(window.id)
            
            key = window_app_user_model_id if window_app_user_model_id else "None"      
           
            if key not in valid_windows:
                valid_windows[key] = [window]
            else:
                valid_windows[key].append(window)

    return valid_windows


def update_running_list():
    #if app.platform == "windows":
    #    return
    
    global RUNNING_APPLICATION_DICT, app_frame_host_cache
    RUNNING_APPLICATION_DICT = {}
    app_frame_host_cache = {}
    running = {}
    foreground_apps = ui.apps(background=False)

    generate_spoken_form_map = {}

    if app.platform == "windows":  
              
        frame_host_apps = ui.apps(name="Application Frame Host", background=False)
        for cur_app in frame_host_apps:
            valid_windows = get_valid_windows_by_app_user_model_id(cur_app)
            for window_app_user_model_id, window_list in valid_windows.items():

                if window_app_user_model_id != "None":
                    mapping = f"{cur_app.name}-::*::-{window_app_user_model_id}"

                    override = get_override_by_app_user_model_id(window_app_user_model_id, cur_app)
                    spoken_forms = override.spoken_forms if override and override.spoken_forms else None

                    if not spoken_forms:
                        spoken_forms = actions.user.create_spoken_forms(source=window_list[-1].title.lower(), words_to_exclude=words_to_exclude,generate_subsequences=False,)

                    for spoken_form in spoken_forms:
                        running[spoken_form] = mapping

                    app_frame_host_cache[window_app_user_model_id.lower()] = True



    for cur_app in foreground_apps:
        #print(f"{cur_app.name} {cur_app.exe}")
        name = cur_app.name.lower()
        exe = os.path.basename(cur_app.exe).lower()
        exe_path = cur_app.exe.lower()
        override = None

        if app.platform == "mac":
            bundle_name = cur_app.bundle.lower()
            RUNNING_APPLICATION_DICT[bundle_name] = [cur_app]

        if exe_path not in RUNNING_APPLICATION_DICT:
            RUNNING_APPLICATION_DICT[exe_path] = [cur_app]
        else:
            RUNNING_APPLICATION_DICT[exe_path].append(cur_app)
        
        if exe not in RUNNING_APPLICATION_DICT:
            RUNNING_APPLICATION_DICT[exe] = [cur_app]
        else:
            RUNNING_APPLICATION_DICT[exe].append(cur_app)

        if name.lower() not in RUNNING_APPLICATION_DICT:
            RUNNING_APPLICATION_DICT[name.lower()] = [cur_app]
        else:
            RUNNING_APPLICATION_DICT[name.lower()].append(cur_app)


        if app.platform == "windows":
            #return

            if exe == "applicationframehost.exe":
                continue
            
            is_windows_app = "windowsapps" in exe_path or "systemapps" in exe_path

            valid_windows = get_valid_windows_by_app_user_model_id(cur_app)

            # if there are no valid windows for the app, let's ignore it.
            if len(valid_windows) <= 0:
                #print(f"{app_user_model_id}; windows = {len(valid_windows)}, should appear in ApplicationFrameHost if it's real...")
                continue

            if (is_windows_app):
                app_user_model_id = get_application_user_model_id(cur_app.pid)
            
                #skip things we know are hosted by the applicationframehost...
                if app_user_model_id.lower() in app_frame_host_cache:
                    continue
                else:
                    override = get_override_by_app_user_model_id(app_user_model_id, cur_app)
            else:
                override = get_override_for_running_app(cur_app)
                # print(f"{cur_app.name}: {override}" )

                uuid = None
                if isinstance(override, Application) or isinstance(override, ApplicationGroup):
                    uuid = override.unique_identifier

                # in many cases, apps will only have one active id, so skip the window-specific logic in that case.     
                if len(valid_windows) > 1:        
                    for window_app_user_model_id, window_list in valid_windows.items():
                        # most applications won't set this
                        if (window_app_user_model_id != "None" 
                            and uuid != window_app_user_model_id):
                            window_override = None
                            window = window_list[-1]

                            window_override = get_override_by_app_user_model_id(window_app_user_model_id, cur_app)

                            spoken_forms = window_override.spoken_forms if window_override and window_override.spoken_forms else None
                            mapping = f"{cur_app.name}-::*::-{window_app_user_model_id}"

                            if spoken_forms:
                                for spoken_form in spoken_forms:
                                    if spoken_form not in running:
                                        running[spoken_form] = mapping
                            else:
                                generate_spoken_form_map[window.title if not window_override else window_override.display_name] = mapping                 
        else:
            override = get_override_for_running_app(cur_app)
            
        if not override:     
            #rundll32 exe & mmc.exe are host application   
            if exe in ["rundll32.exe", "mmc.exe"]:
                for user_model_id, window_list in valid_windows.items():
                    for window in window_list: 
                        mapping = f"{cur_app.name}-::*::-None-::*::-{window.title}"
                        generate_spoken_form_map[window.title] = mapping
            
            if exe != "rundll32.exe":
                generate_spoken_form_map[cur_app.name.lower()] = cur_app.name

        elif override:
            if isinstance(override,ApplicationGroup):
                running[override.group_name] = cur_app.name
                # cycle thru windows and check for subprograms.
                for user_model_id, window_list in valid_windows.items():
                    if user_model_id != "None":
                        continue

                    for display_name, spoken_forms in override.spoken_forms.items():
                        for window in window_list: 
                            if display_name.lower() in window.title.lower():
                                
                                mapping = f"{cur_app.name}-::*::-None-::*::-{window.title}"

                                for spoken_form in spoken_forms:
                                    running[spoken_form] = mapping
                                break

                # ensure the default spoken forms for the group are added.
                if override.group_spoken_forms and len(override.group_spoken_forms) > 0:
                    for spoken_form in override.group_spoken_forms:
                        running[spoken_form] = cur_app.name
                else:
                    generate_spoken_form_map[override.group_name] = cur_app.name
                    
            # check for exclusion
            elif isinstance(override, RunningApplicationExclusion):
                #print(str(override))
                continue
            #otherewise add the things
            else:
                if override.spoken_forms:
                    for spoken_form in override.spoken_forms:
                        mapping = cur_app.name
                        if cur_app.name == "Microsoft Edge":
                            mapping = f"{cur_app.name}-::*::-MSEdge"
                        running[spoken_form] = mapping
                else:
                    generate_spoken_form_map[override.display_name] = cur_app.name   

    if generate_spoken_form_map and len(generate_spoken_form_map) > 0:
        running.update(actions.user.create_spoken_forms_from_map(
            generate_spoken_form_map,
            words_to_exclude=words_to_exclude,
            generate_subsequences=False,
        ))

    #print(running)
    ctx.lists["self.running"] = running

def get_installed_apps():
    global INSTALLED_APPLICATIONS_LIST, INSTALLED_APPLICATIONS_INITIALIZED
    if not INSTALLED_APPLICATIONS_INITIALIZED:
        if app.platform == "windows":
            INSTALLED_APPLICATIONS_LIST = get_installed_windows_apps()
        elif app.platform == "mac":
            INSTALLED_APPLICATIONS_LIST = get_installed_mac_apps()
        INSTALLED_APPLICATIONS_INITIALIZED = True

def process_launch_applications_file(forced: bool = False):
    path = Path(launch_applications_file_path)
    get_installed_apps()

    if not path.exists() or forced:
        all_apps = [*INSTALLED_APPLICATIONS_LIST, *PRESERVED_APPLICATION_LIST]

        grouped = [app for app in all_apps if app.application_group is not None]
        ungrouped = [app for app in all_apps if app.application_group is None]

        grouped = sorted(grouped, key=lambda application: application.application_group)
        ungrouped = sorted(ungrouped, key=lambda application: application.display_name)

        sorted_apps =[*grouped, *ungrouped]

        output = ["Application name, Spoken forms, Exclude from Launch List, Unique Id, Path, Executable Name, Application Group, Default for Applcation Group\n"]
        for application in sorted_apps:
            output.extend(f"{str(application)}\n") 

        with open(path, 'w') as file:
            file.write("".join(output))

process_launch_applications_file()

@resource.watch(running_applications_file_path)
def update_running_exclusions(f):
    global RUNNING_APPLICATION_EXCLUSIONS_DICT
    global RUNNING_APPLICATION_EXCLUSIONS

    RUNNING_APPLICATION_EXCLUSIONS_DICT = {}
    RUNNING_APPLICATION_EXCLUSIONS = []
    rows = list(csv.reader(f))
    for row in rows:
        if (len(row) != 1):
            continue

        splits = row[0].split("=")
        exlcusion_type = None
        if len(splits) == 2:
            parsed_type = splits[0].strip().upper()
            match parsed_type:
                case "EXE":
                    exlcusion_type = ExclusionType.EXECUTABLE

                case "EXECUTABLE":
                    exlcusion_type = ExclusionType.EXECUTABLE

                case "BUNDLE":
                    exlcusion_type = ExclusionType.BUNDLE

                case "PATH":
                    exlcusion_type = ExclusionType.PATH
                
                case "NAME":
                    exlcusion_type = ExclusionType.NAME
                
                case _:
                    print(f"Unknown exclusion type {parsed_type} detected in {running_applications_exclusions_filename}")

        if exlcusion_type:
            data_string = splits[1].strip()
            exclusion = RunningApplicationExclusion(exclusion_type=exlcusion_type, data_string=data_string)
            RUNNING_APPLICATION_EXCLUSIONS.append(exclusion)
            RUNNING_APPLICATION_EXCLUSIONS_DICT[data_string] = exclusion
        else:
            print(f"Malformed application exlucions {row}")

    update_running_list()
    
@resource.watch(launch_applications_file_path)
def update_launch_applications(f):
    global APPLICATIONS_DICT, INSTALLED_APPLICATIONS_LIST, APPLICATIONS_OVERRIDES, INSTALLED_APPLICATIONS_INITIALIZED, WINDOWS_NAME_TO_TALON_NAME
    global PRESERVED_APPLICATION_LIST
    global APPLICATION_GROUPS_DICT
    
    get_installed_apps()

    application_map = {
        app.unique_identifier.lower() : app for app in INSTALLED_APPLICATIONS_LIST
    }

    APPLICATION_GROUPS_DICT = {}  
    APPLICATIONS_OVERRIDES = {}
    WINDOWS_NAME_TO_TALON_NAME = {}
    PRESERVED_APPLICATION_LIST = []
    removed_apps_dict = {}

    must_update_file = False

    rows = list(csv.reader(f))

    if len(rows[1:]) < len(INSTALLED_APPLICATIONS_LIST):
        must_update_file = True
    
    for row in rows[1:]:
        if len(row) == 6 and len(row) == 7 and len(row) == 9:
            print(f"Row {row} malformed; expecting 6-9 entires found {len(row)}")

        group_name = None
        talon_name = None
        if len(row) == 6:
            display_name, spoken_forms, exclude, uid, path, executable_name = (
                [x.strip() or None for x in row])[:6]
        elif len(row) == 7:
            display_name, spoken_forms, exclude, uid, path, executable_name, talon_name = (
                [x.strip() or None for x in row])[:7]        
        # elif len(row) == 8:
        #     display_name, spoken_forms, exclude, uid, path, executable_name, group_name, is_default_for_application_group = (
        #         [x.strip() or None for x in row])[:8]
        
        if spoken_forms.lower() == "none":
            spoken_forms = None
        else:
            spoken_forms = [spoken_form.strip().lower() for spoken_form in spoken_forms.split(";")]
            
        if group_name and group_name.lower() == "none":
            group_name = None

        if talon_name and talon_name.lower() == "none":
            talon_name = None

        if talon_name and talon_name != display_name:
            WINDOWS_NAME_TO_TALON_NAME[display_name] = talon_name

        exclude = False if exclude.lower() == "false" else True
        uid = None if uid.lower() == "none" else uid
        path = None if path.lower() == "none" else path
        executable_name = None if executable_name.lower() == "none" else executable_name

        if not group_name:
            override_app = Application (path=path,
                                        display_name=display_name, 
                                        unique_identifier=uid,
                                        executable_name=executable_name,
                                        exclude = exclude,
                                        spoken_form=spoken_forms,
                                        application_group=None)
        else:
            is_default_for_application_group=is_default_for_application_group.lower()=="true"

            override_app = Application (path=path,
                                        display_name=display_name, 
                                        unique_identifier=uid,
                                        executable_name=executable_name,
                                        exclude = exclude,
                                        spoken_form=spoken_forms,
                                        application_group=group_name,
                                        is_default_for_application_group=is_default_for_application_group)            
        
            if group_name not in APPLICATION_GROUPS_DICT:
                group = ApplicationGroup()
                APPLICATION_GROUPS_DICT[group_name] = group
            else:
                group = APPLICATION_GROUPS_DICT[group_name]

            if is_default_for_application_group:
                group.group_name=group_name
                group.path=path,
                group.executable_name=executable_name,
                group.unique_identifier=uid
                group.group_spoken_forms = spoken_forms if spoken_forms else display_name

                APPLICATION_GROUPS_DICT[executable_name.lower()] = group
                APPLICATION_GROUPS_DICT[path.lower()] = group
            else:
                group.path=path
                group.executable_name=executable_name

                # to do, it is okay perf-wise to generate things here?
                group.spoken_forms[display_name] = spoken_forms if spoken_forms != None else actions.user.create_spoken_forms(display_name.lower(), words_to_exclude=words_to_exclude,generate_subsequences=False,)

        # app has been removed from the OS or is not installed yet.
        # lets preserve this entry for the convenience
        if uid.lower() not in application_map and uid.lower() not in removed_apps_dict:
            removed_apps_dict[uid.lower()] = True
            PRESERVED_APPLICATION_LIST.append(override_app)
    
        APPLICATIONS_OVERRIDES[override_app.display_name] = override_app

        if override_app.executable_name:
            APPLICATIONS_OVERRIDES[override_app.executable_name.lower()] = override_app

        if override_app.path:
            APPLICATIONS_OVERRIDES[override_app.path.lower()] = override_app                   

        if override_app.unique_identifier:
            APPLICATIONS_OVERRIDES[override_app.unique_identifier.lower()] = override_app

    # build the applications dictionary with the overrides applied
    APPLICATIONS_DICT = {}
    for index,application in enumerate(INSTALLED_APPLICATIONS_LIST):
        curr_app = application

        if application.unique_identifier.lower() in APPLICATIONS_OVERRIDES:
            curr_app = APPLICATIONS_OVERRIDES[application.unique_identifier.lower()]
            INSTALLED_APPLICATIONS_LIST[index] = curr_app
        else:
             must_update_file = True

        if curr_app.unique_identifier:
            APPLICATIONS_DICT[curr_app.unique_identifier] = curr_app

        if curr_app.path:
            APPLICATIONS_DICT[curr_app.path] = curr_app

        if curr_app.display_name:
            APPLICATIONS_DICT[curr_app.display_name] = curr_app
    
        if curr_app.executable_name:
            APPLICATIONS_DICT[curr_app.executable_name] = curr_app

    # print("\n".join([str(group) for group in APPLICATION_GROUPS_DICT.values()]))
    if must_update_file:
        print(f"Missing or new application detected, updating {launch_applications_filename}")
        process_launch_applications_file(True)
    else:
        update_running_list()
        if app.platform == "windows":
            rebuild_taskbar_app_list()
        update_launch_list()

@mod.action_class
class Actions:
    def switcher_accessibility_focus(title: str):
        """experimental"""
        rebuild_taskbar_app_list()
        for item in cache:
            if item.title == title:
                item.element.invoke_pattern.invoke()
                break
    def app_switcher_select_index(index: int):
        """"""
        for number, window in enumerate(valid_windows_for_pending_app, 1):
            if index == number:
                window.focus()
                gui_switcher_chooser.hide()
                ctx.tags = []
                break

    def get_running_app(name: str) -> ui.App:
        """Get the first available running app with `name`."""
        # We should use the capture result directly if it's already in the list
        # of running applications. Otherwise, name is from <user.text> and we
        # can be a bit fuzzier
        if name.lower() in RUNNING_APPLICATION_DICT:
            return RUNNING_APPLICATION_DICT[name.lower()]
        else:
            # if len(name) < 3:
            #     raise RuntimeError(
            #         f'Skipped getting app: "{name}" has less than 3 chars.'
            #     )
            # for running_name, full_application_name in ctx.lists[
            #     "self.running"
            # ].items():
            #     if running_name == name or running_name.lower().startswith(
            #         name.lower()
            #     ):
            #         name = full_application_name
            #         break
            result = []
            for application in ui.apps(background=False):
                if application.name == name or application.bundle.lower() == name or (
                    app.platform == "windows"
                    and os.path.basename(application.exe).lower() == name
                ):
                    result.append(application)
            
            if len(result) > 0:
                return result
    
        raise RuntimeError(f'App not running: "{name}"')

    def switcher_focus(name: str):
        """Focus a new application by name"""
        global pending_app 
        global valid_windows_for_pending_app
        pending_app = None
        valid_windows_for_pending_app = None

        splits = name.split("-::*::-")
        app_name = splits[0].lower()
        apps = actions.user.get_running_app(app_name)

        if len(splits) == 3:
            title = splits[2].lower()
            for window in app.windows():
                if title == window.title.lower():
                    window.focus()
                    break
        elif len(splits) == 2:
            application_user_model_id = splits[1]
            for app in apps:
                for window in app.windows():
                    if application_user_model_id == get_application_user_model_for_window(window.id):
                        window.focus()
                        break
        else:
            for app in apps:
                valid_windows = get_valid_windows(app)
                if not valid_windows_for_pending_app:
                    valid_windows_for_pending_app = valid_windows
                else:
                    valid_windows_for_pending_app.extend(valid_windows) 

            if len(valid_windows_for_pending_app) > 1:
                gui_switcher_chooser.show()
                ctx.tags = ["user.app_switcher_selector_showing"] 
            else:
                actions.user.switcher_focus_window(valid_windows_for_pending_app[-1])                
        
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
                print("Failed")
                raise RuntimeError(f"Can't focus window: {window.title}")
            actions.sleep(0.1)
        #print("succeeded")

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

def get_app_overrides():
    return APPLICATIONS_OVERRIDES

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
        for application in APPLICATIONS_DICT.values() 
        if not application.exclude and not application.spoken_forms
    }    

    result = actions.user.create_spoken_forms_from_map(
        sources=launch, 
        words_to_exclude=words_to_exclude,
        generate_subsequences=False,
    )

    customized = {
        spoken_form:  current_app.unique_identifier
        for current_app in APPLICATIONS_DICT.values()
        if current_app.spoken_forms is not None
        for spoken_form in current_app.spoken_forms
    }
    result.update(customized)
    ctx.lists["self.launch"] = result

cache = []

@dataclass
class TaskBarItem:
    title: str
    type: str
    element: Element

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(e for e in element.children if getattr(e, attr) in values)

taskbar = None
ms_tasklist = None
def rebuild_taskbar_app_list(forced: bool = False):
    global cache, taskbar, ms_tasklist

        
    if not taskbar:
        apps = ui.apps(name="Windows Explorer")
        for app in apps:
            for window in app.windows():
                if window.cls == "Shell_TrayWnd":
                    taskbar = window
                    break
            if taskbar:
                ms_tasklist = first_matching_child(taskbar.element, class_name=["MSTaskListWClass"])
                break
                
    if not taskbar:
        actions.app.notify("taskbar window not found")
        return
    
    #update_canvas = forced or len(running_applications.children) != len(cache)
    cache = []
    running_applications_result = {}
    #running = {}
    for e in ms_tasklist.children:

        title = e.name
        splits = title.split(" - ")
        name = splits[0] 
        cache.append(TaskBarItem(title, str(e.control_type), e))
        override = None
        if name in APPLICATIONS_OVERRIDES:
            override = APPLICATIONS_OVERRIDES[name]
            
        if override and override.spoken_forms:
            for form in override.spoken_forms:
                running_applications_result[form] = title
                #running[form] = name if name not in WINDOWS_NAME_TO_TALON_NAME else WINDOWS_NAME_TO_TALON_NAME[name]
        else:
            running_applications_result[name] = title
            #running[name] = name if name not in WINDOWS_NAME_TO_TALON_NAME else WINDOWS_NAME_TO_TALON_NAME[name]

    update_dict = {
        "user.running_applications": running_applications_result, 
        #"user.running": running
    }

    ctx.lists.update(update_dict)

def ui_event(event, arg):
    if event in ("app_launch", "app_close", "app_activate", "app_deactivate"):
        update_running_list()
        if app.platform == "windows":
            rebuild_taskbar_app_list()

def on_ready():
    ui.register("", ui_event)


app.register("ready", on_ready)
