from talon import app
from pathlib import Path
from uuid import UUID
from .application import Application
from.windows_applications import is_known_windows_application
import glob
import os

application_frame_host_path = None
application_frame_host = None
application_frame_host_group = None

if app.platform == "windows":
    from .windows_known_paths import resolve_known_windows_path, PathNotFoundException
    import win32com

    application_frame_host = "applicationframehost.exe"
    application_frame_host_path = os.path.expandvars(os.path.join("%WINDIR%", "System32", application_frame_host))
    application_frame_host_group = "Windows Applications"
    
    # since I can't figure out how to get the target paths from the shell folders,
    # we'll parse the known shortcuts and do it live!?
    windows_application_directories = [
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

    def get_shortcut_target_path(lnk_file):
        # todo: ideally we'd parse the target type here... that would make things more robust
        # windows shortcuts can include applications, Control Panel, and other weird targets.
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(lnk_file)
            return shortcut.Targetpath
        except Exception:
            print(f"Failed to parse {lnk_file}")
            return None
        
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
        stem = Path(short_cut_path).stem
        target_path = get_shortcut_target_path(short_cut_path)


        if target_path:
            shortcut_map[stem] = Path(target_path)
        # some windows shortcuts don't have a path to make things weird (target: Control Panel)
        else:
            shortcut_map[stem] = None

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
                        path = p.resolve()
                        executable_name = p.name  
                        # exclude anything that is NOT an actual executable
                        should_create_entry = is_extension_allowed(p.suffix) 
                        #if not should_create_entry:
                        #    print(f"{executable_name} {path}")

                except:
                    pass
                
                # this isn't very robust, but let's try it..?
                is_known_windows_app, use_application_frame_host = is_known_windows_application(app_user_model_id)
                is_windows_store_app = is_known_windows_app or app_user_model_id.endswith("!App") 

                if is_windows_store_app and use_application_frame_host:
                    executable_name = application_frame_host
                    path = application_frame_host_path

                if should_create_entry and not executable_name:
                    if not is_windows_store_app and display_name in shortcut_map:
                        shortcut_path = shortcut_map[display_name]

                        if shortcut_path:
                            path = shortcut_map[display_name].resolve()
                            executable_name = shortcut_path.name
                            should_create_entry = is_extension_allowed (path.suffix)

                        #if not should_create_entry:
                        #    print(f"{executable_name} {path}")

                #exclude entries that start with http
                if not is_windows_store_app and not executable_name and not path:
                    should_create_entry = should_create_entry and not app_user_model_id.startswith("https://") and not app_user_model_id.startswith("http://") 
                
                new_app = Application(
                    path=str(path) if path else None,
                    display_name=display_name, 
                    unique_identifier= app_user_model_id, 
                    executable_name=executable_name if executable_name else None,
                    exclude=False,
                    spoken_form=None,
                    application_group=application_frame_host_group if is_windows_store_app and use_application_frame_host else None)
            
                #if is_windows_store_app:
                #    print(str(new_app))
                    
                if should_create_entry:
                    if app_user_model_id not in applications_dict:
                        application_list.append(new_app)
                        applications_dict[app_user_model_id] = True
                    else:
                        print(f"Potential duplicate app {new_app}")
        return application_list
else:
    def get_installed_windows_apps() -> list[Application]:
        return []