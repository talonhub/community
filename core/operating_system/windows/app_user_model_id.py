from talon import app, ui

if app.platform == "windows":  
    import win32com
    import ctypes
    from ctypes import wintypes
    import win32con
    import winreg
    from win32com.propsys import propsys, pscon
    import pywintypes
    from win32com.shell import shell, shellcon
    
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
        
    def get_valid_windows_by_app_user_model_id(application,
                                            valid_window_checker: callable, 
                                            empty_window_model_id_mapping=None) -> dict[str, list]:
        valid_windows = {}
        app_list = application
        if not isinstance(app_list, list):
            app_list = [application]

        for cur_app in app_list:
            try:
                windows = cur_app.windows()
            except Exception as e:
                app.notify("installed applications - caught exception {e}")
                print(f"installed applications - caught exception {e}")
                continue

            for window in windows:
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
    def get_application_user_model_id(pid):
        # Open the process
        return None
    
    def get_application_user_model_for_window(hwnd: int):
        return None
    
    def get_valid_windows_by_app_user_model_id(application: ui.App, 
                                            valid_window_checker: callable, 
                                            empty_window_model_id_mapping=None) -> dict[str, list]:
        return {}