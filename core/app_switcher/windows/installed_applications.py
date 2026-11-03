from ...operating_system.windows.data_classes.windows_shortcut import windows_shortcut
from talon import app, ui

from pathlib import Path
from uuid import UUID
from ..common_classes.application import Application
from ...operating_system.windows.windows_known_applications import get_known_windows_application, mmc
import glob
import os

if app.platform == "windows":
    from  ...operating_system.windows.windows_known_paths import resolve_known_windows_path, FOLDERID, PathNotFoundException
    import ctypes
    from ctypes import wintypes
    import winreg

    application_frame_host = "applicationframehost.exe"
    application_frame_host_path = os.path.expandvars(os.path.join("%WINDIR%", "System32", application_frame_host))
    application_frame_host_group = "Windows Applications"

    windows_app_dir = os.path.expandvars(os.path.join("%ProgramFiles%", "WindowsApps"))
    windows_system_app_dir = os.path.expandvars(os.path.join("%WINDIR%", "SystemApps"))
    windows_explorer = Path(os.path.expandvars(os.path.join("%WINDIR%", "explorer.exe"))).resolve()

    # COM goes through the shared helpers in shell_com.py, on the shared COM thread (see
    # the end of this block): initializing COM on Talon's own threads fixes their
    # apartment, which can make Talon's own COM use fail and abort Talon.
    from . import shell_apps, shell_com
    from .com_thread import on_com_thread


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

    def is_extension_allowed(extension):
        return extension.lower() in [".exe", ".msc"]

    def check_should_create_entry(display_name):
        #in windows, many dumb things are added to the apps folder
        return "install" not in display_name.lower() and display_name not in ("This PC")

    def get_installed_windows_apps() -> list[Application]:
        application_list = []
        applications_dict = {}
        # Start menu, desktop and pinned shortcuts by name: the targets of apps the
        # Apps folder doesn't give a path for. Scanned here, on the COM thread.
        shortcut_map = {
            shortcut.name: windows_shortcut(shortcut.name, shortcut.path, shortcut.target, shortcut.arguments)
            for shortcut in shell_apps.shortcuts_by_name().values()
        }
        for item in shell_apps.apps_folder_items():
            path = None
            executable_name = None
            app_user_model_id = item.app_id
            display_name = item.name
            should_create_entry = check_should_create_entry(display_name)

            if should_create_entry:
                try:
                    p = resolve_path_with_guid(app_user_model_id)
                    if p:
                        path = str(p.resolve())
                        executable_name = p.name
                        # exclude anything that is NOT an actual executable
                        should_create_entry = is_extension_allowed(p.suffix)

                        # fix anything with a mmc snap in...
                        if p.suffix and ".msc" == p.suffix.lower():
                           path = mmc
                           executable_name = "mmc.exe"
                except:
                    pass

                if should_create_entry and not executable_name:
                    windows_application_info = get_known_windows_application(app_user_model_id)

                    if windows_application_info:
                        path = windows_application_info.executable_path
                        executable_name = windows_application_info.executable_name

                    elif display_name in shortcut_map:
                        shortcut_info = shortcut_map[display_name]

                        if shortcut_info:
                            if shortcut_info.target_path:
                                path = Path(shortcut_info.target_path).resolve()
                                target_path = Path(shortcut_info.arguments)

                                # Attempt to exclude shortcuts that simply open a folder
                                if path == windows_explorer:
                                    should_create_entry = not os.path.exists(target_path) and os.path.isdir(target_path)
                                else:
                                    should_create_entry = is_extension_allowed (path.suffix)
                                #
                                #print(f"{display_name} {path} {target_path}")
                                executable_name = path.name

                                # fix anything with a mmc snap in...
                                if path.suffix and ".msc" == path.suffix.lower():
                                    path = mmc
                                    executable_name = "mmc.exe"

                if path:
                    should_create_entry = should_create_entry and not str(path).startswith("http")

                new_app = Application(
                    path=str(path) if path else None,
                    display_name=display_name,
                    unique_identifier= app_user_model_id,
                    executable_name=executable_name if executable_name else None,
                    exclude=False,
                    spoken_forms=None,
                    application_group=None)

                # if "Python" in display_name:
                #     print(f"{should_create_entry} {new_app}")

                if should_create_entry:
                    if app_user_model_id not in applications_dict:
                        application_list.append(new_app)
                        applications_dict[app_user_model_id] = True
                    else:
                        print(f"Potential duplicate app {new_app}")
                #else:
                    #print(new_app)
        return application_list


    # Define constants
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

    # Load the necessary DLL
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    # Define the GetApplicationUserModelId function
    GetApplicationUserModelId = kernel32.GetApplicationUserModelId
    GetApplicationUserModelId.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.UINT), wintypes.LPWSTR]
    GetApplicationUserModelId.restype = wintypes.LONG
    # Without these, the returned HANDLE is truncated to a 32-bit int.
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]

    ERROR_INSUFFICIENT_BUFFER = 122
    # The process isn't a packaged app.
    APPMODEL_ERROR_NO_APPLICATION = 15703

    def get_application_user_model_id(pid):
        """The AppUserModelId of a packaged app's process, or None: for processes that
        aren't packaged, or that can't be opened (they may have exited already)."""
        process_handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not process_handle:
            return None

        try:
            # Asking for the length with a NULL buffer fails with ERROR_INVALID_PARAMETER
            # (87) on current Windows, so start with a buffer and grow it if needed.
            length = wintypes.UINT(256)
            buffer = ctypes.create_unicode_buffer(length.value)
            result = GetApplicationUserModelId(process_handle, ctypes.byref(length), buffer)
            if result == ERROR_INSUFFICIENT_BUFFER:
                buffer = ctypes.create_unicode_buffer(length.value)
                result = GetApplicationUserModelId(process_handle, ctypes.byref(length), buffer)

            if result == APPMODEL_ERROR_NO_APPLICATION:
                return None
            if result != 0:
                print(f"get_application_user_model_id({pid}): {ctypes.WinError(result)}")
                return None

            return buffer.value or None
        finally:
            kernel32.CloseHandle(process_handle)

    def get_application_user_model_for_window(hwnd: int):
        try:
            return shell_com.window_property(hwnd, shell_com.PKEY_AppUserModel_ID)
        except Exception:
            return None

    # Enumerating the Apps folder can take a while.
    get_installed_windows_apps = on_com_thread(get_installed_windows_apps, timeout=120)
    get_application_user_model_for_window = on_com_thread(get_application_user_model_for_window)

    def get_valid_windows_by_app_user_model_id(application,
                                            valid_window_checker: callable,
                                            empty_window_model_id_mapping=None) -> dict[str, list]:
        valid_windows = {}
        app_list = application
        if not isinstance(app_list, list):
            app_list = [application]

        for cur_app in app_list:
            for window in cur_app.windows():
                if valid_window_checker(window):
                    window_app_user_model_id = get_application_user_model_for_window(window.id)

                    key = window_app_user_model_id if window_app_user_model_id else "None"

                    if key == "None" and empty_window_model_id_mapping:
                        key = empty_window_model_id_mapping

                    if key not in valid_windows:
                        valid_windows[key] = [window]
                    elif window not in valid_windows[key]:
                        valid_windows[key].append(window)

        return valid_windows

else:
    application_frame_host_path = None
    application_frame_host = None
    application_frame_host_group = None

    def get_installed_windows_apps() -> list[Application]:
        return []

    def get_application_user_model_id(pid):
        # Open the process
        return None

    def get_application_user_model_for_window(hwnd: int):
        return None

    def get_valid_windows_by_app_user_model_id(application: ui.App,
                                            valid_window_checker: callable,
                                            empty_window_model_id_mapping=None) -> dict[str, list]:
        return {}
