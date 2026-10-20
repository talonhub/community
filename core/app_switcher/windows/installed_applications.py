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
    from ctypes import wintypes, POINTER, byref, c_void_p, c_wchar_p, c_ulong, c_int, HRESULT
    import winreg

    application_frame_host = "applicationframehost.exe"
    application_frame_host_path = os.path.expandvars(os.path.join("%WINDIR%", "System32", application_frame_host))
    application_frame_host_group = "Windows Applications"

    windows_app_dir = os.path.expandvars(os.path.join("%ProgramFiles%", "WindowsApps"))
    windows_system_app_dir = os.path.expandvars(os.path.join("%WINDIR%", "SystemApps"))
    windows_explorer = Path(os.path.expandvars(os.path.join("%WINDIR%", "explorer.exe"))).resolve()

    # ------------------------------------------------------------------
    # Minimal pure-ctypes COM shell layer (replaces pywin32 / win32com).
    #
    # We talk to the Windows shell through three COM interfaces:
    #   IShellItem       - a namespace item (a "thing" in the shell)
    #   IEnumShellItems  - iterates the children of a shell item
    #   IPropertyStore   - reads properties (we want AppUserModel.ID)
    # plus IShellLinkW / IPersistFile to read ".lnk" shortcut targets.
    #
    # COM objects are just a pointer to a vtable (an array of function
    # pointers). _com() casts through that vtable to call method #index.
    # ------------------------------------------------------------------
    _ole32 = ctypes.OleDLL("ole32")
    _shell32 = ctypes.OleDLL("shell32")
    _propsys = ctypes.OleDLL("propsys")

    # OleDLL raises OSError automatically when a returned HRESULT indicates
    # failure, so most calls below don't need explicit result checks.
    _ole32.IIDFromString.argtypes = (c_wchar_p, c_void_p)
    _ole32.CoTaskMemFree.restype = None
    _ole32.CoTaskMemFree.argtypes = (c_void_p,)
    _ole32.PropVariantClear.argtypes = (c_void_p,)

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", ctypes.c_ubyte * 8),
        ]

        def __init__(self, guid_string=None):
            super().__init__()
            if guid_string:
                _ole32.IIDFromString(guid_string, byref(self))

    class PROPERTYKEY(ctypes.Structure):
        _fields_ = [("fmtid", GUID), ("pid", wintypes.DWORD)]

    class PROPVARIANT(ctypes.Structure):
        # We never read the union directly; PropVariantToStringAlloc does the
        # conversion for us. 16 bytes of payload covers every variant type
        # on 64-bit Windows.
        _fields_ = [
            ("vt", wintypes.USHORT),
            ("wReserved1", wintypes.USHORT),
            ("wReserved2", wintypes.USHORT),
            ("wReserved3", wintypes.USHORT),
            ("data", ctypes.c_byte * 16),
        ]

    _ole32.CoCreateInstance.argtypes = (
        c_void_p, c_void_p, wintypes.DWORD, c_void_p, POINTER(c_void_p),
    )
    _shell32.SHGetKnownFolderItem.argtypes = (
        c_void_p, wintypes.DWORD, wintypes.HANDLE, c_void_p, POINTER(c_void_p),
    )
    _shell32.SHGetPropertyStoreForWindow.argtypes = (
        wintypes.HWND, c_void_p, POINTER(c_void_p),
    )
    _propsys.PropVariantToStringAlloc.argtypes = (c_void_p, POINTER(c_wchar_p))

    # Interface / class identifiers.
    IID_IShellItem = GUID("{43826D1E-E718-42EE-BC55-A1E261C37BFE}")
    IID_IEnumShellItems = GUID("{70629033-E363-4A28-A567-0DB78006E6D7}")
    IID_IPropertyStore = GUID("{886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99}")
    IID_IShellLinkW = GUID("{000214F9-0000-0000-C000-000000000046}")
    IID_IPersistFile = GUID("{0000010B-0000-0000-C000-000000000046}")
    CLSID_ShellLink = GUID("{00021401-0000-0000-C000-000000000046}")
    BHID_EnumItems = GUID("{94F60519-2850-4924-AA5A-D15E84868039}")
    BHID_PropertyStore = GUID("{0384E1A4-1523-439C-A4C8-AB911052F586}")

    # KNOWNFOLDERID for the virtual "Applications" folder (installed apps,
    # including UWP/Store apps). Not defined by win32com, hence the raw GUID.
    # https://msdn.microsoft.com/en-us/library/dd378457
    FOLDERID_AppsFolder = GUID("{1E87508D-89C2-42F0-8A7E-645A0F50CA58}")

    # The one property we read off each app/window: its AppUserModel.ID.
    PKEY_AppUserModel_ID = PROPERTYKEY(GUID("{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}"), 5)

    SIGDN_NORMALDISPLAY = 0x00000000
    CLSCTX_INPROC_SERVER = 0x1
    COINIT_APARTMENTTHREADED = 0x2

    # vtable slot 0/1/2 are always IUnknown's QueryInterface/AddRef/Release.
    _IUNKNOWN_RELEASE = 2
    _IUNKNOWN_QUERYINTERFACE = 0

    def _com(this, index, restype, *argtypes):
        """Return a callable for method #index of the COM object `this`."""
        vtable = ctypes.cast(this, POINTER(POINTER(c_void_p)))[0]
        proto = ctypes.WINFUNCTYPE(restype, c_void_p, *argtypes)
        return proto(vtable[index])

    def _release(obj):
        if obj:
            _com(obj, _IUNKNOWN_RELEASE, c_ulong)(obj)

    def _bind_to_handler(item, bhid, riid):
        """IShellItem::BindToHandler -> a new interface pointer (caller releases)."""
        out = c_void_p()
        _com(item, 3, HRESULT, c_void_p, POINTER(GUID), POINTER(GUID), POINTER(c_void_p))(
            item, None, byref(bhid), byref(riid), byref(out)
        )
        return out

    def _item_display_name(item, sigdn=SIGDN_NORMALDISPLAY):
        """IShellItem::GetDisplayName."""
        pname = c_wchar_p()
        _com(item, 5, HRESULT, c_ulong, POINTER(c_wchar_p))(item, sigdn, byref(pname))
        try:
            return pname.value
        finally:
            _ole32.CoTaskMemFree(pname)

    def _store_app_user_model_id(store):
        """Read AppUserModel.ID (a string) from an open IPropertyStore.

        VT_EMPTY (property absent) converts to "" here, matching pywin32's
        ToString() behavior.
        """
        pv = PROPVARIANT()
        # IPropertyStore::GetValue (slot 5)
        _com(store, 5, HRESULT, POINTER(PROPERTYKEY), POINTER(PROPVARIANT))(
            store, byref(PKEY_AppUserModel_ID), byref(pv)
        )
        try:
            out = c_wchar_p()
            _propsys.PropVariantToStringAlloc(byref(pv), byref(out))
            try:
                return out.value or ""
            finally:
                _ole32.CoTaskMemFree(out)
        finally:
            _ole32.PropVariantClear(byref(pv))

    def _item_app_user_model_id(item):
        """AppUserModel.ID for a shell item, via its IPropertyStore.

        Raises OSError if the item has no property store or the value can't
        be read (the shell's equivalent of pywin32's pywintypes.error).
        """
        store = _bind_to_handler(item, BHID_PropertyStore, IID_IPropertyStore)
        try:
            return _store_app_user_model_id(store)
        finally:
            _release(store)

    def iter_known_folder_items(folder_id):
        """Yield each child IShellItem of a known folder.

        Each yielded pointer is released automatically once the consumer
        advances the iterator, so the loop body must not retain it.
        """
        item = c_void_p()
        _shell32.SHGetKnownFolderItem(
            byref(folder_id), 0, None, byref(IID_IShellItem), byref(item)
        )
        try:
            enum = _bind_to_handler(item, BHID_EnumItems, IID_IEnumShellItems)
            try:
                while True:
                    child = c_void_p()
                    fetched = c_ulong(0)
                    # IEnumShellItems::Next (slot 3); returns S_FALSE at the end.
                    _com(enum, 3, HRESULT, c_ulong, POINTER(c_void_p), POINTER(c_ulong))(
                        enum, 1, byref(child), byref(fetched)
                    )
                    if not fetched.value or not child.value:
                        break
                    try:
                        yield child
                    finally:
                        _release(child)
            finally:
                _release(enum)
        finally:
            _release(item)

    # COM must be initialized on this thread before any of the calls above.
    # S_FALSE (already initialized) doesn't raise; RPC_E_CHANGED_MODE (the
    # thread is already in a different apartment) is fine for our purposes.
    try:
        _ole32.CoInitializeEx(None, COINIT_APARTMENTTHREADED)
    except OSError:
        pass

    #print(f"{windows_app_dir} {windows_system_app_dir}")
    def get_desktop_path():
        return resolve_known_windows_path(FOLDERID.Desktop)

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

    def get_shortcut_info(lnk_file) -> windows_shortcut:
        # todo: ideally we'd parse the target type here... that would make things more robust
        # windows shortcuts can include applications, Control Panel, and other weird targets.
        name = Path(lnk_file).stem
        target_path = None
        arguments = ""

        link = c_void_p()
        _ole32.CoCreateInstance(
            byref(CLSID_ShellLink), None, CLSCTX_INPROC_SERVER,
            byref(IID_IShellLinkW), byref(link),
        )
        try:
            # Load the .lnk file through IPersistFile.
            persist = c_void_p()
            _com(link, _IUNKNOWN_QUERYINTERFACE, HRESULT, POINTER(GUID), POINTER(c_void_p))(
                link, byref(IID_IPersistFile), byref(persist)
            )
            try:
                # IPersistFile::Load (slot 5), STGM_READ (0).
                _com(persist, 5, HRESULT, c_wchar_p, wintypes.DWORD)(persist, str(lnk_file), 0)
            finally:
                _release(persist)

            try:
                # IShellLinkW::GetPath (slot 3); pass NULL for the find-data.
                buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
                _com(link, 3, HRESULT, c_wchar_p, c_int, c_void_p, wintypes.DWORD)(
                    link, buf, wintypes.MAX_PATH, None, 0
                )
                target_path = buf.value or None
            except OSError:
                target_path = None

            try:
                # IShellLinkW::GetArguments (slot 10). Empty string (not None)
                # when there are no arguments, matching WScript.Shell so the
                # downstream Path(shortcut_info.arguments) stays valid.
                argbuf = ctypes.create_unicode_buffer(1024)
                _com(link, 10, HRESULT, c_wchar_p, c_int)(link, argbuf, 1024)
                arguments = argbuf.value
            except OSError:
                arguments = ""
        except OSError:
            # Couldn't read the shortcut at all; fall through with what we have.
            pass
        finally:
            _release(link)

        return windows_shortcut(str(name), lnk_file, target_path, arguments)

    def is_extension_allowed(extension):
        return extension.lower() in [".exe", ".msc"]

    def check_should_create_entry(display_name):
        #in windows, many dumb things are added to the apps folder
        return "install" not in display_name.lower() and display_name not in ("This PC")

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
        for item in iter_known_folder_items(FOLDERID_AppsFolder):
            path = None
            executable_name = None
            display_name = None
            app_user_model_id = None

            try:
                app_user_model_id = _item_app_user_model_id(item)
            except OSError:
                continue

            display_name = _item_display_name(item, SIGDN_NORMALDISPLAY)
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

    def get_application_user_model_id(pid):
        # Open the process
        process_handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
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
            store = c_void_p()
            # SHGetPropertyStoreForWindow -> IPropertyStore for the window.
            _shell32.SHGetPropertyStoreForWindow(hwnd, byref(IID_IPropertyStore), byref(store))
            try:
                return _store_app_user_model_id(store) or None
            finally:
                _release(store)
        except Exception:
            return None

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
