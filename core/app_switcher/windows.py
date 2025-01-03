from talon import app
from pathlib import Path
from uuid import UUID
from .application import Application
from.windows_applications import get_known_windows_application, WindowsShortcut, mmc
import glob
import os

if app.platform == "windows":
    from .windows_known_paths import resolve_known_windows_path, PathNotFoundException
    import win32com
    import ctypes
    from ctypes import wintypes
    import win32con
    import winreg
    from win32com.propsys import propsys, pscon
    import pywintypes
    from win32com.shell import shell, shellcon

    application_frame_host = "applicationframehost.exe"
    application_frame_host_path = os.path.expandvars(os.path.join("%WINDIR%", "System32", application_frame_host))
    application_frame_host_group = "Windows Applications"
    
    windows_app_dir = os.path.expandvars(os.path.join("%ProgramFiles%", "WindowsApps"))
    windows_system_app_dir = os.path.expandvars(os.path.join("%WINDIR%", "SystemApps"))

    #print(f"{windows_app_dir} {windows_system_app_dir}")
    def get_desktop_path():
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:

            desktop = winreg.QueryValueEx(key, "Desktop")[0]

        return os.path.expandvars(desktop)

    # since I can't figure out how to get the target paths from the shell folders,
    # we'll parse the known shortcuts and do it live!?
    windows_application_directories = [
        get_desktop_path(), 
        "%AppData%/Microsoft/Windows/Start Menu/Programs",
        "%ProgramData%/Microsoft/Windows/Start Menu/Programs",
        "%AppData%/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar",
    ]

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

    def get_shortcut_info(lnk_file)-> WindowsShortcut:
        # todo: ideally we'd parse the target type here... that would make things more robust
        # windows shortcuts can include applications, Control Panel, and other weird targets.
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lnk_file)
        name = Path(lnk_file).stem
        try:
            arguments = shortcut.Arguments
        except:
            arguments = None

        try:
            target_path = shortcut.TargetPath
        except:
            target_path = None

        return WindowsShortcut(str(name), lnk_file, target_path, arguments )
        
    def is_extension_allowed(extension):
        return extension.lower() in [".exe", ".msc"]
    
    def check_should_create_entry(display_name):
        #in windows, many dumb things are added to the apps folder
        return "install" not in display_name.lower()

    shortcut_paths = []
    for path in windows_application_directories:
        full_path = os.path.expandvars(path)
        shortcut_paths.extend(glob.glob(os.path.join(full_path, '**/*.lnk'), recursive=True))

    shortcut_map = {}
    for short_cut_path in shortcut_paths:
        shortcut =  get_shortcut_info(short_cut_path)
        if shortcut:
            shortcut_map[shortcut.display_name] = shortcut
            
    def get_installed_windows_apps() -> list[Application]:
        application_list = []
        applications_dict = {}
        for item in enum_known_folder(FOLDERID_AppsFolder):
            path = None
            executable_name = None
            display_name = None
            app_user_model_id = None

            try:
                property_store = item.BindToHandler(
                    None, shell.BHID_PropertyStore, propsys.IID_IPropertyStore
                )
                app_user_model_id = property_store.GetValue(
                    pscon.PKEY_AppUserModel_ID
                ).ToString()

            except pywintypes.error:
                continue

            display_name = item.GetDisplayName(shellcon.SIGDN_NORMALDISPLAY)
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
                                executable_name = path.name
                                should_create_entry = is_extension_allowed (path.suffix)

                                # fix anything with a mmc snap in...
                                if path.suffix and ".msc" == path.suffix.lower():
                                    path = mmc
                                    executable_name = "mmc.exe"
                        

                is_url_maybe = str(path).startswith("http") if path else False

                new_app = Application(
                    path=str(path) if path else None,
                    display_name=display_name, 
                    unique_identifier= app_user_model_id, 
                    executable_name=executable_name if executable_name else None,
                    exclude=False,
                    spoken_form=None,
                    application_group=None)
                    
                if "Python" in display_name:
                    print(f"{should_create_entry} {new_app}")
                
                if should_create_entry and not is_url_maybe:
                    if app_user_model_id not in applications_dict:
                        application_list.append(new_app)
                        applications_dict[app_user_model_id] = True
                    else:
                        print(f"Potential duplicate app {new_app}")
                #else:
                    #print(new_app)
        return application_list
    

    # Define constants

    # Load the necessary DLL
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    # Define the GetApplicationUserModelId function
    GetApplicationUserModelId = kernel32.GetApplicationUserModelId
    GetApplicationUserModelId.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.UINT), wintypes.LPWSTR]
    GetApplicationUserModelId.restype = wintypes.LONG

    def get_application_user_model_id(pid):
        # Open the process
        process_handle = kernel32.OpenProcess(win32con.PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not process_handle:
            raise ctypes.WinError(ctypes.get_last_error())

        try:
            # Get the length of the ApplicationUserModelId
            length = wintypes.UINT(0)
            result = GetApplicationUserModelId(process_handle, ctypes.byref(length), None)

            # we expect error 122 in this algorithm
            if result != 122:
                raise ctypes.WinError(result)

            # Allocate buffer for the ApplicationUserModelId
            buffer = ctypes.create_unicode_buffer(length.value)
            result = GetApplicationUserModelId(process_handle, ctypes.byref(length), buffer)
            if result != 0:
                raise ctypes.WinError(result)

            return buffer.value
        finally:
            kernel32.CloseHandle(process_handle)

    def get_application_user_model_for_window(hwnd: int):    
        try:
            property_store = propsys.SHGetPropertyStoreForWindow(hwnd, propsys.IID_IPropertyStore)
            window_app_user_model_id = property_store.GetValue(pscon.PKEY_AppUserModel_ID)
            return window_app_user_model_id.GetValue()
        except:
            return None

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