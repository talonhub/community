# from talon import app, ui

# if app.platform == "windows":  
#     import ctypes
#     from ctypes import wintypes
    
#     # Load the necessary DLL
#     kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
#     user32 = ctypes.WinDLL('user32', use_last_error=True)
#     shell32 = ctypes.WinDLL('shell32', use_last_error=True)
#     ole32 = ctypes.WinDLL('ole32', use_last_error=True)

#     PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

#     HRESULT = ctypes.c_long

#     class GUID(ctypes.Structure):
#         _fields_ = [
#             ("Data1", wintypes.DWORD),
#             ("Data2", wintypes.WORD),
#             ("Data3", wintypes.WORD),
#             ("Data4", wintypes.BYTE * 8),
#         ]

#     class PROPERTYKEY(ctypes.Structure):
#         _fields_ = [
#             ("fmtid", GUID),
#             ("pid", wintypes.DWORD),
#         ]

#     class PROPVARIANT_VALUE(ctypes.Union):
#         _fields_ = [
#             ("llVal", ctypes.c_longlong),
#             ("lVal", ctypes.c_long),
#             ("bVal", ctypes.c_byte),
#             ("boolVal", wintypes.VARIANT_BOOL),
#             ("pwszVal", wintypes.LPWSTR),
#             ("punkVal", ctypes.c_void_p),
#             ("_padding", ctypes.c_byte * 16),
#         ]

#     class PROPVARIANT(ctypes.Structure):
#         _anonymous_ = ("value",)
#         _fields_ = [
#             ("vt", wintypes.USHORT),
#             ("wReserved1", wintypes.USHORT),
#             ("wReserved2", wintypes.USHORT),
#             ("wReserved3", wintypes.USHORT),
#             ("value", PROPVARIANT_VALUE),
#         ]

#     class IPropertyStoreVtbl(ctypes.Structure):
#         _fields_ = [
#             ("QueryInterface", ctypes.WINFUNCTYPE(HRESULT, ctypes.c_void_p, ctypes.POINTER(GUID), ctypes.POINTER(ctypes.c_void_p))),
#             ("AddRef", ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)),
#             ("Release", ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)),
#             ("GetCount", ctypes.WINFUNCTYPE(HRESULT, ctypes.c_void_p, ctypes.POINTER(wintypes.DWORD))),
#             ("GetAt", ctypes.WINFUNCTYPE(HRESULT, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(PROPERTYKEY))),
#             ("GetValue", ctypes.WINFUNCTYPE(HRESULT, ctypes.c_void_p, ctypes.POINTER(PROPERTYKEY), ctypes.POINTER(PROPVARIANT))),
#             ("SetValue", ctypes.WINFUNCTYPE(HRESULT, ctypes.c_void_p, ctypes.POINTER(PROPERTYKEY), ctypes.POINTER(PROPVARIANT))),
#             ("Commit", ctypes.WINFUNCTYPE(HRESULT, ctypes.c_void_p)),
#         ]

#     class IPropertyStore(ctypes.Structure):
#         _fields_ = [("lpVtbl", ctypes.POINTER(IPropertyStoreVtbl))]

#     IID_IPropertyStore = GUID(
#         0x886D8EEB,
#         0x8CF2,
#         0x4446,
#         (ctypes.c_ubyte * 8)(0x8D, 0x02, 0xCD, 0xBA, 0x1D, 0xBD, 0xCF, 0x99),
#     )

#     PKEY_AppUserModel_ID = PROPERTYKEY(
#         GUID(
#             0x9F4C2855,
#             0x9F79,
#             0x4B39,
#             (ctypes.c_ubyte * 8)(0xA8, 0xD0, 0xE1, 0xD4, 0x2D, 0xE1, 0xD5, 0xF3),
#         ),
#         5,
#     )

#     # Define the GetApplicationUserModelId function
#     GetApplicationUserModelId = kernel32.GetApplicationUserModelId
#     GetApplicationUserModelId.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.UINT), wintypes.LPWSTR]
#     GetApplicationUserModelId.restype = wintypes.LONG

#     SHGetPropertyStoreForWindow = shell32.SHGetPropertyStoreForWindow
#     SHGetPropertyStoreForWindow.argtypes = [wintypes.HWND, ctypes.POINTER(GUID), ctypes.POINTER(ctypes.c_void_p)]
#     SHGetPropertyStoreForWindow.restype = HRESULT

#     PropVariantClear = ole32.PropVariantClear
#     PropVariantClear.argtypes = [ctypes.POINTER(PROPVARIANT)]
#     PropVariantClear.restype = HRESULT

#     def _raise_if_failed(hr: int, message: str):
#         if hr < 0:
#             raise OSError(f"{message}: 0x{hr & 0xffffffff:08x}")

#     def _get_property_store_for_window(hwnd: int):
#         store_ptr = ctypes.c_void_p()
#         hr = SHGetPropertyStoreForWindow(hwnd, ctypes.byref(IID_IPropertyStore), ctypes.byref(store_ptr))
#         _raise_if_failed(hr, "SHGetPropertyStoreForWindow failed")
#         if not store_ptr.value:
#             return None
#         return ctypes.cast(store_ptr, ctypes.POINTER(IPropertyStore))

#     def _get_property_store_value_string(store, key: PROPERTYKEY):
#         propvar = PROPVARIANT()
#         hr = store.contents.lpVtbl.contents.GetValue(store, ctypes.byref(key), ctypes.byref(propvar))
#         _raise_if_failed(hr, "IPropertyStore.GetValue failed")

#         try:
#             if propvar.vt == 31 and propvar.pwszVal:
#                 return propvar.pwszVal
#             return None
#         finally:
#             PropVariantClear(ctypes.byref(propvar))

#     def get_application_user_model_id(pid):
#         # Open the process
#         process_handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
#         if not process_handle:
#             raise ctypes.WinError(ctypes.get_last_error())

#         try:
#             # Get the length of the ApplicationUserModelId
#             length = wintypes.UINT(0)
#             result = GetApplicationUserModelId(process_handle, ctypes.byref(length), None)

#             # we expect error 122 in this algorithm
#             if result != 122:
#                 raise ctypes.WinError(result)

#             # Allocate buffer for the ApplicationUserModelId
#             buffer = ctypes.create_unicode_buffer(length.value)
#             result = GetApplicationUserModelId(process_handle, ctypes.byref(length), buffer)
#             if result != 0:
#                 raise ctypes.WinError(result)

#             return buffer.value
#         finally:
#             kernel32.CloseHandle(process_handle)

#     def get_application_user_model_for_window(hwnd: int):    
#         try:
#             store = _get_property_store_for_window(hwnd)
#             if not store:
#                 return None

#             try:
#                 return _get_property_store_value_string(store, PKEY_AppUserModel_ID)
#             finally:
#                 store.contents.lpVtbl.contents.Release(store)
#         except OSError:
#             return None
        
#     def get_valid_windows_by_app_user_model_id(application,
#                                             valid_window_checker: callable, 
#                                             empty_window_model_id_mapping=None) -> dict[str, list]:
#         valid_windows = {}
#         app_list = application
#         if not isinstance(app_list, list):
#             app_list = [application]

#         for cur_app in app_list:
#             try:
#                 windows = cur_app.windows()
#             except Exception as e:
#                 app.notify("installed applications - caught exception {e}")
#                 print(f"installed applications - caught exception {e}")
#                 continue

#             for window in windows:
#                 if valid_window_checker(window):
#                     window_app_user_model_id = get_application_user_model_for_window(window.id)
                    
#                     key = window_app_user_model_id if window_app_user_model_id else "None"
                        
#                     if key == "None" and empty_window_model_id_mapping:
#                         key = empty_window_model_id_mapping

#                     if key not in valid_windows:
#                         valid_windows[key] = [window]
#                     elif window not in valid_windows[key]:
#                         valid_windows[key].append(window)

#         return valid_windows
# else:    
#     def get_application_user_model_id(pid):
#         # Open the process
#         return None
    
#     def get_application_user_model_for_window(hwnd: int):
#         return None
    
#     def get_valid_windows_by_app_user_model_id(application: ui.App, 
#                                             valid_window_checker: callable, 
#                                             empty_window_model_id_mapping=None) -> dict[str, list]:
#         return {}