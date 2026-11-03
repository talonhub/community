import ctypes
import os
import shlex
import subprocess
import time
from pathlib import Path
import csv
import talon
from talon import Context, Module, actions, app, cron, imgui, ui, resource
from .windows import app_identity, window_filter
from .windows.installed_applications import get_installed_windows_apps, get_valid_windows_by_app_user_model_id, get_application_user_model_id, get_application_user_model_for_window
from .mac.installed_applications import get_installed_mac_apps
from .common_classes.exclusion import ExclusionType, RunningApplicationExclusion
from typing import Union
from .common_classes.application import Application, ApplicationGroup
import re
from talon.windows.ax import Element
from dataclasses import dataclass, asdict
import json

import platform
hostname = platform.node()
base_script_directory = os.path.dirname(os.path.realpath(__file__))
csv_directory = os.path.join(base_script_directory, talon.app.platform, hostname)
running_applications_exclusions_filename = "running_applications_exclusions.csv"
running_applications_file_path = os.path.normcase(
    os.path.join(csv_directory, running_applications_exclusions_filename)
)

launch_applications_json = "launch_applications.json"
launch_applications_json = os.path.normcase(
    os.path.join(csv_directory, launch_applications_json)
)

if not os.path.exists(csv_directory):
    # Create the directory
    os.makedirs(csv_directory)

SW_RESTORE = 9
# Executables that host other apps (MMC consoles, Control Panel applets, Parallels' Mac
# app launchers): launch_applications.json entries aren't looked up by them.
HOST_EXECUTABLES = {"mmc.exe", "rundll32.exe", "dllhost.exe"}
# Executables whose one process can carry several apps as the taskbar shows them
# (browsers with installed PWAs, packaged-app hosts): never stand in for an app by
# process, or "focus edge" could bring up a PWA living in Edge's process.
SHARED_HOST_EXECUTABLES = HOST_EXECUTABLES | {
    "msedge.exe",
    "chrome.exe",
    "brave.exe",
    "vivaldi.exe",
    "opera.exe",
    "firefox.exe",
    "applicationframehost.exe",
}
# focus_targets values for launch-list apps that aren't running.
LAUNCH_PREFIX = "launch::"

mod = Module()
mod.tag("app_switcher_selector_showing", desc="Indicates the app_switcher_selector_showing")
mod.list("running", desc="all running applications")
mod.list("launch", desc="all launchable applications")
mod.list("running_applications", desc="all running applications")
mod.list("focus_targets", desc="running applications, then launchable ones (for focus)")

ctx = Context()

# a list of the currently running application names
RUNNING_APPLICATION_DICT = {}

# Windows: running list value (lowercase) -> its app_identity.AppIdentity list
# (several when identities share a name: two Edge profiles' browser windows)
RUNNING_IDENTITIES = {}

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
    "Google",
    "google",
    "install",
    "installer",
    "Microsoft",
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
    return m.running


@mod.capture(rule="{self.focus_targets}")
def focus_target(m) -> str:
    "A running application's name, or a launchable one's (prefixed launch::)"
    return m.focus_targets


@mod.capture(rule="{self.launch}")
def launch_applications(m) -> str:
    "Returns a single application name"
    return m.launch

def get_application_by_app_user_model_id(uuid) -> Application:
    if uuid.lower() in APPLICATIONS_DICT:
        return APPLICATIONS_DICT[uuid.lower()]
    return None
    
def get_override_by_app_user_model_id(uuid, application: ui.App):
    if uuid.lower() in APPLICATIONS_OVERRIDES:
        return APPLICATIONS_OVERRIDES[uuid.lower()]
    
    return get_override_for_running_app(application)

def get_override_for_running_app(application: ui.App) -> Union[Application | ApplicationGroup | RunningApplicationExclusion | None]:
    name = application.name
    bundle_name = application.bundle
    exe_path = str(Path(application.exe).resolve()).lower()
    executable_name = os.path.basename(application.exe).lower()

    if exe_path in APPLICATION_GROUPS_DICT:
        return APPLICATION_GROUPS_DICT[exe_path]
    elif executable_name in APPLICATION_GROUPS_DICT:
        return APPLICATION_GROUPS_DICT[executable_name]
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

def get_window_class(window: ui.Window) -> bool:
    cls = None
    if not window:
        return None
    try:
        cls = window.cls
    except Exception as e:
        print(f"exception = {e}")
        #app.notify("get_window_class exception - switcher askbar")
        cls = None
    
    return cls

def is_valid_explorer_window(window: ui.Window) -> bool:
    """A File Explorer window (Talon reports the class as "CabinetWClass")."""
    return is_window_valid(window) and (get_window_class(window) or "").lower() in ["explorerwclass", "cabinetwclass"]


def is_window_valid(window: ui.Window) -> bool:
    """Returns true if this window is valid for focusing"""
    if app.platform == "windows":
        # The rule Alt+Tab uses: minimized windows count, while hidden (cloaked)
        # system windows don't. A size check gets both wrong, as minimized windows
        # report a tiny rect.
        try:
            return (
                len(window.title) > 0
                and "chrome legacy window" not in window.title.lower()
                and window_filter.is_switchable(window.id)
            )
        except Exception:
            return False
    return (
        not window.hidden
        # There are many fake windows with empty titles -- this excludes them.
        and len(window.title) > 0
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

def get_spoken_form_mapping_for_host_app(host_app, valid_window_checker=is_window_valid, host_cache=None, empty_window_model_id_mapping=None):
    spoken_form_map = {}
    for cur_app in host_app:
        valid_windows = get_valid_windows_by_app_user_model_id(cur_app, valid_window_checker)
        for window_app_user_model_id, window_list in valid_windows.items():

            if window_app_user_model_id != "None":
                mapping = f"{cur_app.name}-::*::-{window_app_user_model_id}"

                override = get_override_by_app_user_model_id(window_app_user_model_id, cur_app)
                spoken_forms = override.spoken_forms if override and override.spoken_forms else None
                
                if not spoken_forms:
                    if override and override.display_name:
                        spoken_forms = actions.user.create_spoken_forms(source=override.display_name, words_to_exclude=words_to_exclude,generate_subsequences=False,)
                    else:
                        spoken_forms = actions.user.create_spoken_forms(source=window_list[-1].title.lower(), words_to_exclude=words_to_exclude,generate_subsequences=False,)
                
                for spoken_form in spoken_forms:
                    spoken_form_map[spoken_form] = mapping

                if window_app_user_model_id.lower() not in RUNNING_APPLICATION_DICT:
                    RUNNING_APPLICATION_DICT[window_app_user_model_id.lower()] = [window_list[-1]]

                if host_cache:
                    host_cache[window_app_user_model_id.lower()] = True

            else:
                RUNNING_APPLICATION_DICT[empty_window_model_id_mapping.lower()] = [window_list[-1]]
                mapping = f"{cur_app.name}-::*::-None"

                override = get_override_by_app_user_model_id(empty_window_model_id_mapping, cur_app)
                spoken_forms = override.spoken_forms if override and override.spoken_forms else None

                if not spoken_forms:
                    if override and override.display_name:
                        spoken_forms = actions.user.create_spoken_forms(source=override.display_name, words_to_exclude=words_to_exclude,generate_subsequences=False,)
                    else:
                        spoken_forms = actions.user.create_spoken_forms(source=window_list[-1].title.lower(), words_to_exclude=words_to_exclude,generate_subsequences=False,)                
                
                for spoken_form in spoken_forms:
                    spoken_form_map[spoken_form] = mapping

    return spoken_form_map

def populate_spoken_forms_for_valid_windows(application, 
                                            app_name,
                                            override: Union[Application | ApplicationGroup | RunningApplicationExclusion | None],  
                                            windows: list, 
                                            running_list):
    global RUNNING_APPLICATION_DICT
    spoken_forms_to_generate = {}

    for window_app_user_model_id, window_list in windows.items():
        # print(f"hit it {window_app_user_model_id}")
        # most applications won't set this
        if (window_app_user_model_id != "None"): 
            #and uuid != window_app_user_model_id):
            window_override = None
            window = window_list[-1]

            window_override = get_override_by_app_user_model_id(window_app_user_model_id, application)

            spoken_forms = window_override.spoken_forms if window_override and window_override.spoken_forms else None
            mapping = f"{application.name}-::*::-{window_app_user_model_id}"

            if window_app_user_model_id.lower() not in RUNNING_APPLICATION_DICT:
                RUNNING_APPLICATION_DICT[window_app_user_model_id.lower()] = window_list
            else:
                RUNNING_APPLICATION_DICT[window_app_user_model_id.lower()].extend(window_list)

            if spoken_forms:
                for spoken_form in spoken_forms:
                    if spoken_form not in running_list:
                        running_list[spoken_form] = mapping
            else:
                spoken_forms_to_generate[window.title if not window_override else window_override.display_name] = mapping 

        #todo: is it "safe" to assume that none will always map to the default app?
        elif override:
            add_spoken_forms_from_override(running_list, spoken_forms_to_generate, app_name, override)

    return spoken_forms_to_generate

def get_exclusion_for_running_app(application: ui.App) -> RunningApplicationExclusion | None:
    """The running_applications_exclusions.csv entry matching the app, if any."""
    exe_path = str(Path(application.exe).resolve()).lower()
    for key in (exe_path, os.path.basename(application.exe).lower(), application.bundle, application.name):
        if key and key in RUNNING_APPLICATION_EXCLUSIONS_DICT:
            return RUNNING_APPLICATION_EXCLUSIONS_DICT[key]
    return None


def get_override_for_window(identity: app_identity.AppIdentity, application: ui.App):
    """The launch_applications.json entry (or exclusion, or group) for a window's app.

    Apps with an AppUserModelID (packaged apps, PWAs, File Explorer) and MMC consoles
    are looked up by their id only: looking them up by executable would give every PWA
    Microsoft Edge's entry, and every MMC console whichever mmc.exe entry came last.
    """
    exclusion = get_exclusion_for_running_app(application)
    if exclusion:
        return exclusion
    if identity.model_id:
        return APPLICATIONS_OVERRIDES.get(identity.model_id.lower())
    if identity.document:
        return APPLICATIONS_OVERRIDES.get(identity.document_id.lower()) if identity.document_id else None
    exe_path = str(Path(application.exe).resolve()).lower()
    group = APPLICATION_GROUPS_DICT.get(exe_path) or APPLICATION_GROUPS_DICT.get(os.path.basename(exe_path))
    if group:
        return group
    # The entry with the app's taskbar name: several entries can share an executable
    # (Visual Studio's developer prompts all run cmd.exe, like "Command Prompt").
    named = APPLICATIONS_OVERRIDES.get(identity.name)
    if isinstance(named, Application):
        return named
    return get_override_for_running_app(application)


def update_running_list_windows():
    """The running list on Windows: one entry per app as the taskbar groups and names
    them (app_identity), with launch_applications.json's spoken forms and display names
    and the exclusions applied.

    Values are the apps' taskbar names; RUNNING_APPLICATION_DICT maps each (lowercase)
    to its windows, most recently used first, so get_running_app and switcher_focus find
    exactly that app's windows (one MMC console, one PWA). Executable names and paths
    still map to Talon's apps.
    """
    global RUNNING_APPLICATION_DICT, RUNNING_IDENTITIES
    RUNNING_APPLICATION_DICT = {}
    RUNNING_IDENTITIES = {}
    running = {}
    generate_spoken_form_map = {}
    groups = {}
    seen = set()
    # Talon apps (processes) by their exe/name keys, and the identities each exe
    # carries; filed under those keys at the end, only where that's unambiguous.
    process_keys = {}
    identities_by_exe = {}
    for window in ui.windows():
        if window.id in seen:
            # Consoles are listed under both cmd and conhost.
            continue
        seen.add(window.id)
        if not is_window_valid(window):
            continue
        try:
            application = window.app
            exe = application.exe
        except Exception:
            continue
        identity = app_identity.resolve(window.id, application.name)
        groups.setdefault(identity.key, (identity, application, []))[2].append(window)
        base = os.path.basename(exe).lower()
        identities_by_exe.setdefault(base, set()).add(identity.key)
        process_keys.setdefault(base, []).append(
            (application, {exe.lower(), base, application.name.lower()})
        )
    app_identity.forget_others(seen)

    order = window_filter.z_order()
    names = {}
    for identity, application, windows in groups.values():
        override = get_override_for_window(identity, application)
        if isinstance(override, RunningApplicationExclusion):
            continue
        value = identity.name
        names.setdefault(value.lower(), []).extend(windows)
        RUNNING_IDENTITIES.setdefault(value.lower(), []).append(identity)
        for key in (identity.model_id, identity.document_id):
            if key:
                RUNNING_APPLICATION_DICT[key.lower()] = windows
        if isinstance(override, ApplicationGroup):
            forms = override.group_spoken_forms
            if isinstance(forms, str):
                generate_spoken_form_map[forms] = value
            elif forms:
                for form in forms:
                    running[form.strip()] = value
            else:
                generate_spoken_form_map[override.group_name] = value
        elif override and override.spoken_forms:
            for form in override.spoken_forms:
                running[form.strip()] = value
        else:
            source = override.display_name if override and override.display_name else identity.name
            generate_spoken_form_map[source.strip()] = value
    for key, windows in names.items():
        RUNNING_APPLICATION_DICT[key] = sorted(windows, key=lambda w: order.get(w.id, 1 << 30))
    # Executable names and paths still find Talon's app, for processes that carry a
    # single app; never a shared host (msedge.exe with PWAs), and never in place of
    # an app's own name ("microsoft edge" is the browser's windows, not the process).
    for base, entries in process_keys.items():
        if base in SHARED_HOST_EXECUTABLES or len(identities_by_exe.get(base, ())) > 1:
            continue
        for application, keys in entries:
            for key in keys:
                if not key or key in names:
                    continue
                bucket = RUNNING_APPLICATION_DICT.setdefault(key, [])
                if application not in bucket:
                    bucket.append(application)

    if generate_spoken_form_map:
        running.update(actions.user.create_spoken_forms_from_map(
            generate_spoken_form_map,
            words_to_exclude=words_to_exclude,
            generate_subsequences=False,
        ))
    ctx.lists["self.running"] = running
    refresh_focus_targets()


def refresh_focus_targets():
    """user.focus_targets: the running list, then launch-list spoken forms not already
    taken by a running app (running wins), their values prefixed with LAUNCH_PREFIX."""
    try:
        running = dict(ctx.lists.get("self.running", {}) or {})
        launch = dict(ctx.lists.get("self.launch", {}) or {})
    except Exception:
        return
    targets = dict(running)
    for spoken, value in launch.items():
        if spoken not in targets:
            targets[spoken] = LAUNCH_PREFIX + str(value)
    ctx.lists["self.focus_targets"] = targets


_refresh_job = None


def schedule_running_list_refresh():
    """Rebuild the running list a moment after window events, coalescing bursts."""
    global _refresh_job
    if _refresh_job is not None:
        cron.cancel(_refresh_job)

    def run():
        global _refresh_job
        _refresh_job = None
        update_running_list()

    _refresh_job = cron.after("150ms", run)


def live_identity_windows(name: str) -> list:
    """The running list app `name`'s windows that still exist and still belong to it,
    most recently used first."""
    keys = {identity.key for identity in RUNNING_IDENTITIES.get(name.lower(), ())}
    windows = [w for w in RUNNING_APPLICATION_DICT.get(name.lower(), []) if isinstance(w, ui.Window)]
    live = []
    for window in windows:
        try:
            if not ctypes.windll.user32.IsWindow(window.id) or not is_window_valid(window):
                continue
            if keys and app_identity.resolve(window.id, window.app.name).key not in keys:
                continue
        except Exception:
            continue
        live.append(window)
    return live


def launch_identity(name: str):
    """Start the running list app `name` (whose windows are all gone) by its launch
    list entry or AppUserModelID."""
    identities = RUNNING_IDENTITIES.get(name.lower()) or [None]
    identity = identities[0]
    model_id = identity and (identity.window_id or identity.process_id)
    candidates = [c for c in (model_id, identity and identity.document_id, name) if c]
    for candidate in candidates:
        entry = APPLICATIONS_DICT.get(candidate.lower())
        if entry is not None and entry.unique_identifier:
            actions.user.switcher_launch(entry.unique_identifier)
            return
    if model_id:
        actions.user.switcher_launch(model_id)
        return
    if identity is not None and identity.exe_path:
        actions.user.switcher_launch(identity.exe_path)
        return
    raise RuntimeError(f'No open windows and nothing to launch for "{name}"')


def update_running_list():
    if app.platform == "windows":
        update_running_list_windows()
        return

    global RUNNING_APPLICATION_DICT, app_frame_host_cache
    RUNNING_APPLICATION_DICT = {}
    app_frame_host_cache = {}
    running = {}
    foreground_apps = ui.apps(background=False)

    generate_spoken_form_map = {}

    if app.platform == "windows":  
        #populate application frame hosted apps
        frame_host_apps = ui.apps(name="Application Frame Host", background=False)
        valid_windows = get_valid_windows_by_app_user_model_id(frame_host_apps, is_window_valid)

        for key, _ in valid_windows.items():
            app_frame_host_cache[key] = True
            app_frame_host_cache[key.lower()] = True
                
        if len(frame_host_apps) > 0:
            generate_spoken_form_map.update(populate_spoken_forms_for_valid_windows(frame_host_apps[0], 
                                                                                    "Application Frame Host", 
                                                                                    None, 
                                                                                    valid_windows, 
                                                                                    running))
        
        #populate explorer hosted apps
        explorer_apps = ui.apps(name="Windows Explorer", background=False)
        override = get_override_by_app_user_model_id("Microsoft.Windows.Explorer", explorer_apps[0])

        valid_windows = get_valid_windows_by_app_user_model_id(explorer_apps, is_valid_explorer_window, "Microsoft.Windows.Explorer")
        generate_spoken_form_map.update(populate_spoken_forms_for_valid_windows(explorer_apps[0], 
                                                                                "Windows Explorer", 
                                                                                override,  
                                                                                valid_windows, 
                                                                                running))

    for application in foreground_apps:
        is_name_valid = True
        name = application.name.lower().strip()
        app_name = application.name
        exe = os.path.basename(application.exe).lower()
        exe_path = application.exe.lower()
        override = None

        if not name:
            is_name_valid = False
            if exe_path:
                # print(f"{exe_path} has no application name. Using exe_path")
                app_name = exe_path
            else:
                continue
            
        if app.platform == "windows" and exe in ["applicationframehost.exe", "explorer.exe"]:
            continue


        # on windows, let's check for valid windows before continuing.
        if app.platform == "windows":
            valid_windows = get_valid_windows_by_app_user_model_id(application=application, valid_window_checker=is_window_valid)
            if len(valid_windows) <= 0:
                continue

        if app.platform == "mac":
            bundle_name = application.bundle.lower()
            RUNNING_APPLICATION_DICT[bundle_name.lower()] = [application]

        if exe_path not in RUNNING_APPLICATION_DICT:
            RUNNING_APPLICATION_DICT[exe_path.lower()] = [application]
        else:
            RUNNING_APPLICATION_DICT[exe_path.lower()].append(application)
        
        if exe not in RUNNING_APPLICATION_DICT:
            RUNNING_APPLICATION_DICT[exe.lower()] = [application]
        else:
            RUNNING_APPLICATION_DICT[exe.lower()].append(application)

        if is_name_valid:
            if name.lower() not in RUNNING_APPLICATION_DICT:
                RUNNING_APPLICATION_DICT[name.lower()] = [application]
            else:
                RUNNING_APPLICATION_DICT[name.lower()].append(application)
            

        if app.platform == "windows":
            
            is_windows_app = "windowsapps" in exe_path or "systemapps" in exe_path
            # None when the process isn't packaged after all, or has already exited.
            app_user_model_id = get_application_user_model_id(application.pid) if is_windows_app else None

            if (app_user_model_id):
                #skip things we know are hosted by the applicationframehost...
                if app_user_model_id.lower() in app_frame_host_cache:
                    continue
                else:
                    override = get_override_by_app_user_model_id(app_user_model_id, application)

                RUNNING_APPLICATION_DICT[app_user_model_id.lower()] = [application]
            else:
                override = get_override_for_running_app(application)
                # print(f"{cur_app.name}: {override}" )

                if len(valid_windows) > 1 or len(valid_windows) == 1 and "None" not in valid_windows:                   
                    uuid = None
                    if isinstance(override, Application) or isinstance(override, ApplicationGroup):
                        uuid = override.unique_identifier

                    spoken_forms_requiring_generation = populate_spoken_forms_for_valid_windows(application, app_name, override, valid_windows, running)
                    generate_spoken_form_map.update(spoken_forms_requiring_generation)

                    # skip further processing.
                    continue

        else:
            override = get_override_for_running_app(application)

        if not override:     
            #rundll32 exe & mmc.exe are host application   
            if exe in ["rundll32.exe", "mmc.exe"]:
                for user_model_id, window_list in valid_windows.items():
                    for window in window_list: 
                        mapping = f"{application.name}-::*::-None-::*::-{window.title}"
                        generate_spoken_form_map[window.title] = mapping
            else:
                generate_spoken_form_map[application.name.lower()] = app_name

        elif override:
            # if isinstance(override,ApplicationGroup):
            #     running[override.group_name] = application.name
            #     # cycle thru windows and check for subprograms.
            #     for user_model_id, window_list in valid_windows.items():
            #         if user_model_id != "None":
            #             continue

            #         for display_name, spoken_forms in override.spoken_forms.items():
            #             for window in window_list: 
            #                 if display_name.lower() in window.title.lower():
                                
            #                     mapping = f"{application.name}-::*::-None-::*::-{window.title}"

            #                     for spoken_form in spoken_forms:
            #                         running[spoken_form] = mapping
            #                     break

            #     # ensure the default spoken forms for the group are added.
            #     if override.group_spoken_forms and len(override.group_spoken_forms) > 0:
            #         for spoken_form in override.group_spoken_forms:
            #             running[spoken_form] = application.name
            #     else:
            #         generate_spoken_form_map[override.group_name] = application.name
                add_spoken_forms_from_override(running, 
                                            generate_spoken_form_map, 
                                            app_name,
                                            override)   

    if generate_spoken_form_map and len(generate_spoken_form_map) > 0:
        running.update(actions.user.create_spoken_forms_from_map(
            generate_spoken_form_map,
            words_to_exclude=words_to_exclude,
            generate_subsequences=False,
        ))

    #print(running)
    ctx.lists["self.running"] = running

def add_spoken_forms_from_override(running_list, 
                                   generate_spoken_form_map, 
                                   app_name, 
                                   override):
    if isinstance(override, RunningApplicationExclusion):
        #print(str(override))
        return 
    
    if override.spoken_forms:
        for spoken_form in override.spoken_forms:
            running_list[spoken_form.strip()] = app_name
    else:
        generate_spoken_form_map[override.display_name.strip()] = app_name

def get_installed_apps():
    global INSTALLED_APPLICATIONS_LIST, INSTALLED_APPLICATIONS_INITIALIZED
    if not INSTALLED_APPLICATIONS_INITIALIZED:
        if app.platform == "windows":
            INSTALLED_APPLICATIONS_LIST = get_installed_windows_apps()
        elif app.platform == "mac":
            INSTALLED_APPLICATIONS_LIST = get_installed_mac_apps()
        INSTALLED_APPLICATIONS_INITIALIZED = True

def generate_spoken_forms(application: Application) -> list[str] | None:
    """The spoken forms "launch" would generate from the app's display name, so they
    can be written into launch_applications.json where the user can see and edit them.
    None if they can't be made (e.g. the action isn't registered yet at startup)."""
    if not application.display_name:
        return None
    try:
        forms = actions.user.create_spoken_forms(
            source=application.display_name,
            words_to_exclude=words_to_exclude,
            generate_subsequences=False,
        )
    except Exception as e:
        print(f"Couldn't generate spoken forms for {application.display_name}: {e!r}")
        return None
    forms = list(dict.fromkeys(form for form in forms if form))
    return forms or None


def process_launch_applications_file(forced: bool = False):
    json_path = Path(launch_applications_json)
    get_installed_apps()

    if not json_path.exists():
        # A brand-new file: every entry is new, so record its generated spoken forms.
        for application in INSTALLED_APPLICATIONS_LIST:
            if application.spoken_forms is None:
                application.spoken_forms = generate_spoken_forms(application)

    if not json_path.exists() or forced:
        all_apps = [*INSTALLED_APPLICATIONS_LIST, *PRESERVED_APPLICATION_LIST]

        grouped = [app for app in all_apps if app.application_group is not None]
        ungrouped = [app for app in all_apps if app.application_group is None]

        grouped = sorted(grouped, key=lambda application: application.application_group)
        ungrouped = sorted(ungrouped, key=lambda application: application.display_name)

        sorted_apps =[*grouped, *ungrouped]

        with open(json_path, "w") as json_file:
            json.dump([asdict(application) for application in sorted_apps], json_file, indent = 4)

process_launch_applications_file()

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


# The exclusions file is optional: watching a file that doesn't exist fails when Talon
# starts ("cannot access local variable 'obj'").
if os.path.exists(running_applications_file_path):
    update_running_exclusions = resource.watch(running_applications_file_path)(update_running_exclusions)

@resource.watch(launch_applications_json)
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

    # Read JSON file
    with open(launch_applications_json, "r") as json_file:
        applications = json.load(json_file)

    if len(applications) < len(INSTALLED_APPLICATIONS_LIST):
        must_update_file = True

    # Convert JSON dictionaries to application objects
    applications = [Application(**application) for application in applications]
    
    for application in applications:
        application_group = application.application_group
        if application_group:
            is_default_for_application_group=application.is_default_for_application_group

            if application_group not in APPLICATION_GROUPS_DICT:
                group = ApplicationGroup()
                APPLICATION_GROUPS_DICT[application_group] = group
            else:
                group = APPLICATION_GROUPS_DICT[application_group]

            if is_default_for_application_group:
                group.group_name=application_group
                group.path=application.path,
                group.executable_name=application.executable_name,
                group.unique_identifier=application.unique_identifier
                group.group_spoken_forms = application.spoken_forms if application.spoken_forms else application.display_name

                APPLICATION_GROUPS_DICT[application.executable_name.lower()] = group
                APPLICATION_GROUPS_DICT[application.path.lower()] = group
            else:
                group.path=application.path
                group.executable_name=application.executable_name

                # to do, it is okay perf-wise to generate things here?
                group.spoken_forms[application.display_name] = application.spoken_forms if application.spoken_forms != None else actions.user.create_spoken_forms(application.display_name.lower(), words_to_exclude=words_to_exclude,generate_subsequences=False,)

        # app has been removed from the OS or is not installed yet.
        # lets preserve this entry for the convenience
        if application.unique_identifier.lower() not in application_map and application.unique_identifier.lower() not in removed_apps_dict:
            removed_apps_dict[application.unique_identifier.lower()] = True
            PRESERVED_APPLICATION_LIST.append(application)
    
        APPLICATIONS_OVERRIDES[application.display_name] = application

        # Not by host executables: every Parallels "(Mac)" shortcut runs rundll32.exe,
        # every MMC console mmc.exe; their windows are told apart by command line.
        is_host = (application.executable_name or "").lower() in HOST_EXECUTABLES
        if application.executable_name and not is_host:
            APPLICATIONS_OVERRIDES[application.executable_name.lower()] = application

        if application.path and not is_host:
            APPLICATIONS_OVERRIDES[application.path.lower()] = application

        if application.unique_identifier:
            APPLICATIONS_OVERRIDES[application.unique_identifier.lower()] = application

    # build the applications dictionary with the overrides applied
    APPLICATIONS_DICT = {}
    for index,application in enumerate(INSTALLED_APPLICATIONS_LIST):
        curr_app = application

        if application.unique_identifier.lower() in APPLICATIONS_OVERRIDES:
            curr_app = APPLICATIONS_OVERRIDES[application.unique_identifier.lower()]
            INSTALLED_APPLICATIONS_LIST[index] = curr_app
        else:
            # Newly found app: write its generated spoken forms into the file.
            if curr_app.spoken_forms is None:
                curr_app.spoken_forms = generate_spoken_forms(curr_app)
            must_update_file = True

        if curr_app.unique_identifier:
            APPLICATIONS_DICT[curr_app.unique_identifier.lower()] = curr_app

        if curr_app.path:
            APPLICATIONS_DICT[curr_app.path.lower()] = curr_app

        if curr_app.display_name:
            APPLICATIONS_DICT[curr_app.display_name.lower()] = curr_app
    
        if curr_app.executable_name:
            APPLICATIONS_DICT[curr_app.executable_name.lower()] = curr_app

    # Names for apps the shell has no name for, in the thumbnail switcher too.
    if app.platform == "windows":
        app_identity.register_name_override(
            lambda app_user_model_id: getattr(get_application_by_app_user_model_id(app_user_model_id), "display_name", None)
        )

    # print("\n".join([str(group) for group in APPLICATION_GROUPS_DICT.values()]))
    if must_update_file:
        print(f"Missing or new application detected, updating {launch_applications_json}")
        process_launch_applications_file(True)
    else:
        update_running_list()
        if app.platform == "windows":
            rebuild_taskbar_app_list()
        update_launch_list()

@mod.action_class
class Actions:
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
    
    def switcher_select_index(index: int):
        """Focuses the selected window index when requested"""
        for number, window in enumerate(valid_windows_for_pending_app, 1):
            if index == number:
                window.focus()
                gui_switcher_chooser.hide()
                ctx.tags = []
                break

    def switcher_show_desktop():
        """"""
        actions.key("super-d")

    def switcher_focus(name: str):
        """Focus a new application by name"""
        global pending_app 
        global valid_windows_for_pending_app
        pending_app = None
        valid_windows_for_pending_app = None

        if app.platform == "windows" and name.startswith(LAUNCH_PREFIX):
            # A launch-list app named by "focus": focus it if it runs, else start it.
            actions.user.switcher_launch(name[len(LAUNCH_PREFIX):])
            return

        splits = name.split("-::*::-")
        app_name = splits[0]

        if app.platform == "windows" and len(splits) == 1:
            # The running list's apps are app identities (as the taskbar groups them):
            # focus that identity's windows, never its process (a browser's process also
            # carries its PWAs), and launch it when none are open any more.
            windows = live_identity_windows(app_name)
            if windows:
                actions.user.switcher_focus_window(windows[0])
            else:
                launch_identity(app_name)
            return

        apps = actions.user.get_running_app(app_name)
        # On Windows, running list entries map to that app's windows, most recently
        # used first.
        windows = [item for item in apps if isinstance(item, ui.Window)]
        if windows and len(splits) == 1:
            actions.user.switcher_focus_window(windows[0])
            return
        apps = [item for item in apps if isinstance(item, ui.App)] or [w.app for w in windows]
        valid_window_checker = is_window_valid

        app_name = app_name.lower()
        if app_name == "windows explorer":
            valid_window_checker = is_valid_explorer_window

        if len(splits) == 3:
            title = splits[2].lower()
            for window in [w for a in set(apps) for w in a.windows()]:
                if title == window.title.lower():
                    actions.user.switcher_focus_window(window)
                    break
        elif len(splits) == 2:
            application_user_model_id = splits[1]
            valid_windows_for_pending_app = []
            if application_user_model_id.lower() in RUNNING_APPLICATION_DICT:
                valid_windows_for_pending_app = RUNNING_APPLICATION_DICT[application_user_model_id.lower()]
            else:
                for running_app in set(apps):
                    for window in running_app.windows():
                        if valid_window_checker(window) and str(application_user_model_id) == str(get_application_user_model_for_window(window.id)):
                            valid_windows_for_pending_app.append(window)
            
            # if len(valid_windows_for_pending_app) > 1:
            #     gui_switcher_chooser.show()
            #     ctx.tags = ["user.app_switcher_selector_showing"] 
            # else:
            actions.user.switcher_focus_window(valid_windows_for_pending_app[-1]) 
                
        else:
            actions.user.switcher_focus_app(apps[-1])
            # for app in set(apps):
            #     valid_windows = get_valid_windows(app)
            #     if not valid_windows_for_pending_app:
            #         valid_windows_for_pending_app = valid_windows
            #     else:
            #         valid_windows_for_pending_app.extend(valid_windows) 

            # if len(valid_windows_for_pending_app) > 1:
            #     gui_switcher_chooser.show()
            #     ctx.tags = ["user.app_switcher_selector_showing"] 
            # else:
            #actions.user.switcher_focus_window(valid_windows_for_pending_app[-1])                
        
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
        if app.platform == "windows" and ctypes.windll.user32.IsIconic(window.id):
            # Focusing doesn't bring a minimized window back by itself.
            ctypes.windll.user32.ShowWindow(window.id, SW_RESTORE)
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
            application_info = get_application_by_app_user_model_id(path)

            if application_info:
                # Running as an app identity: its live windows only (stale or another
                # identity's windows would bring up the wrong app); none left -> launch.
                key = next(
                    (k for k in (path.lower(), application_info.display_name.lower()) if k in RUNNING_IDENTITIES),
                    None,
                )
                if key is not None:
                    windows = live_identity_windows(key)
                    if windows:
                        actions.user.switcher_focus_window(windows[0])
                        return
                elif path.lower() in RUNNING_APPLICATION_DICT:
                    RUNNING_APPLICATION_DICT[path.lower()][-1].focus()
                    return
                elif application_info.display_name.lower() in RUNNING_APPLICATION_DICT:
                    # print(f"{application_info.display_name} found")
                    RUNNING_APPLICATION_DICT[application_info.display_name.lower()][-1].focus()
                    return

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

    def switcher_show_applications():
        """Show applications"""
        if gui_applications.showing:
            gui_applications.hide()
        else:
            gui_applications.show()

    def switcher_hide_applications():
        """Show applications"""
        gui_applications.hide()

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
def gui_applications(gui: imgui.GUI):
    gui.text("Applications (spoken forms: display name)")
    gui.line()
    
    for display_name, spoken_form in launch_cache:
        gui.text(f"{display_name}: {spoken_form}")

    gui.spacer()
    if gui.button("Running close"):
        actions.user.switcher_hide_running()

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

launch_cache = {}
def update_launch_list():
    global launch_cache 
    launch_cache = {}

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

    # Spoken forms stored in the file. Disabled (excluded) apps stay out, now that
    # generated forms are stored too.
    customized = {
        spoken_form:  current_app.unique_identifier
        for current_app in APPLICATIONS_DICT.values()
        if current_app.spoken_forms is not None and not current_app.exclude
        for spoken_form in current_app.spoken_forms
    }

    result.update(customized)
    launch.update(customized)
    ctx.lists["self.launch"] = result
    refresh_focus_targets()

    launch_cache = {
        application.display_name : application.display_name 
        for application in APPLICATIONS_DICT.values() 
        if not application.exclude and not application.spoken_forms
    }    

    customized_cache = {
        current_app.display_name : spoken_form 
        for current_app in APPLICATIONS_DICT.values()
        if current_app.spoken_forms is not None and not current_app.exclude
        for spoken_form in current_app.spoken_forms
    }

    launch_cache.update(customized_cache)
    launch_cache = sorted(launch_cache.items())
    
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
    return
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
    elif app.platform == "windows" and event in ("win_open", "win_close", "win_show", "win_hide"):
        # A window can come or go while its process stays (a browser window closing
        # while the browser's PWAs keep the process alive): no app event then.
        schedule_running_list_refresh()

def on_ready():
    ui.register("", ui_event)


app.register("ready", on_ready)
