# from talon import Context, Module, actions, app, ui, clip
# import os

# if app.platform == "windows":
#     # NOTE: pywin32 (win32com / win32gui) has no free-threaded build, so the
#     # current explorer path is read by driving the Shell COM interfaces
#     # directly through ctypes, which works with or without the GIL.
#     # import ctypes
#     # from ctypes import POINTER, byref, c_void_p, c_long, c_ulong, c_longlong, c_ushort
#     # from ctypes import wintypes

# #from ...core.operating_system.windows.windows_known_paths import resolve_known_windows_path, FOLDERID

# mod = Module()
# apps = mod.apps

# apps.windows_explorer = r"""
# os: windows
# and app.name: Windows Explorer
# and win.title: /File Explorer/
# os: windows
# and app.name: Windows-Explorer
# os: windows
# and app.exe: /^explorer\.exe$/i
# and win.title: /File Explorer/
# """

# # # many commands should work in most save/open dialog.
# # # note the "show options" stuff won't work unless work
# # # unless the path is displayed in the title, which is rare for those
# # apps.windows_file_browser = """
# # os: windows
# # and app.name: /.*/
# # and title: /(Save|Open|Browse|Select)/
# # """

# ctx = Context()
# ctx.matches = r"""
# app: windows_explorer
# # app: windows_file_browser
# """

# user_path = os.path.expanduser("~")
# directories_to_remap = {}
# directories_to_exclude = {}


# if app.platform == "windows":
#     is_windows = True
  
#     known_paths_to_resolve = {
#         # "Desktop": FOLDERID.Desktop,
#         # "Documents": FOLDERID.Documents,
#         # "Downloads": FOLDERID.Documents,
#         # "Music": FOLDERID.Music,
#         # "Pictures": FOLDERID.Pictures,
#         # "Videos": FOLDERID.Profile
#     }

#     for key, value in known_paths_to_resolve.items():
#         # try:
#         #     path = resolve_known_windows_path(value)
#         # except Exception as e:
#         ath = None

#     directories_to_exclude = [
#         "",
#         "Run",
#         "Task Switching",
#         "Task View",
#         "This PC",
#         "File Explorer",
#         "Program Manager",
#     ]

# if app.platform == "windows":
#     # ---- Minimal ctypes COM plumbing (free-threaded compatible) ------------
#     S_OK = 0
#     S_FALSE = 1
#     RPC_E_CHANGED_MODE = -2147417850  # 0x80010106
#     COINIT_APARTMENTTHREADED = 0x2
#     CLSCTX_ALL = 0x17
#     VT_I4 = 3
#     GA_ROOT = 2
#     MAX_PATH = 260

#     class GUID(ctypes.Structure):
#         _fields_ = [
#             ("Data1", ctypes.c_uint32),
#             ("Data2", ctypes.c_uint16),
#             ("Data3", ctypes.c_uint16),
#             ("Data4", ctypes.c_ubyte * 8),
#         ]

#     # 64-bit VARIANT is 24 bytes; padded so it is passed by value correctly.
#     class VARIANT(ctypes.Structure):
#         _fields_ = [
#             ("vt", c_ushort),
#             ("wReserved1", c_ushort),
#             ("wReserved2", c_ushort),
#             ("wReserved3", c_ushort),
#             ("val", c_longlong),
#             ("pad", c_longlong),
#         ]

#     _ole32 = ctypes.WinDLL("ole32")
#     _shell32 = ctypes.WinDLL("shell32")
#     _user32 = ctypes.WinDLL("user32")

#     _ole32.CoCreateInstance.argtypes = [
#         POINTER(GUID), c_void_p, wintypes.DWORD, POINTER(GUID), POINTER(c_void_p)
#     ]
#     _ole32.CoCreateInstance.restype = c_long
#     _ole32.IIDFromString.argtypes = [ctypes.c_wchar_p, POINTER(GUID)]
#     _ole32.IIDFromString.restype = c_long
#     _shell32.SHGetPathFromIDListW.argtypes = [c_void_p, ctypes.c_wchar_p]
#     _shell32.SHGetPathFromIDListW.restype = wintypes.BOOL
#     _user32.GetForegroundWindow.restype = wintypes.HWND
#     _user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
#     _user32.GetAncestor.restype = wintypes.HWND

#     def _guid(s: str) -> GUID:
#         g = GUID()
#         if _ole32.IIDFromString(s, byref(g)) != S_OK:
#             raise OSError(f"IIDFromString failed for {s}")
#         return g

#     CLSID_ShellWindows = _guid("{9BA05972-F6A8-11CF-A442-00A0C90A8F39}")
#     IID_IShellWindows = _guid("{85CB6900-4D95-11CF-960C-0080C7F4EE85}")
#     IID_IServiceProvider = _guid("{6D5140C1-7436-11CE-8034-00AA006009FA}")
#     SID_STopLevelBrowser = _guid("{4C96BE40-915C-11CF-99D3-00AA004AE837}")
#     IID_IShellBrowser = _guid("{000214E2-0000-0000-C000-000000000046}")
#     IID_IFolderView = _guid("{CDE725B0-CCC9-4519-917E-325D72FAB4CE}")
#     IID_IPersistFolder2 = _guid("{1AC3D9F0-175C-11D1-95BE-00609797EA4F}")

#     def _vtable_call(this, index, restype, *args):
#         """Call the vtable method at `index` on a raw COM interface pointer.

#         Each entry in `args` is a (ctype, value) tuple for that argument.
#         """
#         vtbl = ctypes.cast(this, POINTER(c_void_p))[0]
#         fn_addr = ctypes.cast(vtbl, POINTER(c_void_p))[index]
#         proto = ctypes.WINFUNCTYPE(restype, c_void_p, *[a[0] for a in args])
#         return proto(fn_addr)(this, *[a[1] for a in args])

#     def _release(ptr):
#         if ptr:
#             _vtable_call(ptr, 2, c_ulong)

#     def _path_from_browser(disp, hwnd_fg):
#         # IUnknown::QueryInterface for IServiceProvider
#         sp = c_void_p()
#         if _vtable_call(disp, 0, c_long,
#                         (POINTER(GUID), byref(IID_IServiceProvider)),
#                         (POINTER(c_void_p), byref(sp))) != S_OK or not sp:
#             return None
#         try:
#             # IServiceProvider::QueryService -> IShellBrowser
#             sb = c_void_p()
#             if _vtable_call(sp, 3, c_long,
#                             (POINTER(GUID), byref(SID_STopLevelBrowser)),
#                             (POINTER(GUID), byref(IID_IShellBrowser)),
#                             (POINTER(c_void_p), byref(sb))) != S_OK or not sb:
#                 return None
#             try:
#                 # IOleWindow::GetWindow, then match the owning top-level window
#                 hwnd = wintypes.HWND()
#                 if _vtable_call(sb, 3, c_long,
#                                 (POINTER(wintypes.HWND), byref(hwnd))) != S_OK:
#                     return None
#                 if _user32.GetAncestor(hwnd, GA_ROOT) != hwnd_fg:
#                     return None

#                 # IShellBrowser::QueryActiveShellView -> IShellView
#                 sv = c_void_p()
#                 if _vtable_call(sb, 15, c_long,
#                                 (POINTER(c_void_p), byref(sv))) != S_OK or not sv:
#                     return None
#                 try:
#                     # IShellView -> IFolderView
#                     fv = c_void_p()
#                     if _vtable_call(sv, 0, c_long,
#                                     (POINTER(GUID), byref(IID_IFolderView)),
#                                     (POINTER(c_void_p), byref(fv))) != S_OK or not fv:
#                         return None
#                     try:
#                         # IFolderView::GetFolder -> IPersistFolder2
#                         pf2 = c_void_p()
#                         if _vtable_call(fv, 5, c_long,
#                                         (POINTER(GUID), byref(IID_IPersistFolder2)),
#                                         (POINTER(c_void_p), byref(pf2))) != S_OK or not pf2:
#                             return None
#                         try:
#                             # IPersistFolder2::GetCurFolder -> PIDL
#                             pidl = c_void_p()
#                             if _vtable_call(pf2, 5, c_long,
#                                             (POINTER(c_void_p), byref(pidl))) != S_OK or not pidl:
#                                 return None
#                             try:
#                                 buf = ctypes.create_unicode_buffer(MAX_PATH)
#                                 if _shell32.SHGetPathFromIDListW(pidl, buf):
#                                     return buf.value
#                                 return None
#                             finally:
#                                 _ole32.CoTaskMemFree(pidl)
#                         finally:
#                             _release(pf2)
#                     finally:
#                         _release(fv)
#                 finally:
#                     _release(sv)
#             finally:
#                 _release(sb)
#         finally:
#             _release(sp)

#     def _get_active_explorer_path_windows():
#         hwnd_fg = _user32.GetForegroundWindow()
#         if not hwnd_fg:
#             return None

#         hr = _ole32.CoInitializeEx(None, COINIT_APARTMENTTHREADED)
#         need_uninit = hr in (S_OK, S_FALSE)
#         try:
#             shell_windows = c_void_p()
#             if _ole32.CoCreateInstance(
#                 byref(CLSID_ShellWindows), None, CLSCTX_ALL,
#                 byref(IID_IShellWindows), byref(shell_windows),
#             ) != S_OK or not shell_windows:
#                 return None
#             try:
#                 # IShellWindows::get_Count
#                 count = c_long(0)
#                 if _vtable_call(shell_windows, 7, c_long,
#                                 (POINTER(c_long), byref(count))) != S_OK:
#                     return None
#                 for i in range(count.value):
#                     # IShellWindows::Item(VARIANT index) -> IDispatch
#                     var = VARIANT()
#                     var.vt = VT_I4
#                     var.val = i
#                     disp = c_void_p()
#                     if _vtable_call(shell_windows, 8, c_long,
#                                     (VARIANT, var),
#                                     (POINTER(c_void_p), byref(disp))) != S_OK or not disp:
#                         continue
#                     try:
#                         path = _path_from_browser(disp, hwnd_fg)
#                         if path is not None:
#                             return path
#                     finally:
#                         _release(disp)
#                 return None
#             finally:
#                 _release(shell_windows)
#         finally:
#             if need_uninit:
#                 _ole32.CoUninitialize()


# def get_active_explorer_path():
#     if app.platform != "windows":
#         return None
#     path = _get_active_explorer_path_windows()
#     print(f"got path {path} from COM")
#     return path

# @ctx.action_class("user")
# class UserActions:
#     def file_manager_open_parent():
#         actions.key("alt-up")

#     def file_manager_current_path():
#         path = get_active_explorer_path()

#         # if path in directories_to_remap:
#         #     path = directories_to_remap[path]

#         # if path in directories_to_exclude:
#         #     actions.user.file_manager_hide_pickers()
#         #     path = ""

#         return path

#     def file_manager_terminal_here():
#         actions.key("ctrl-l")
#         actions.insert("cmd.exe")
#         actions.key("enter")

#     def file_manager_show_properties():
#         """Shows the properties for the file"""
#         actions.key("alt-enter")

#     def file_manager_open_directory(path: str):
#         """opens the directory that's already visible in the view"""
#         actions.key("ctrl-l")
#         toolbar = ui.active_window().element.find_one(automation_id = "TextBox", max_depth=0)
#         toolbar.value_pattern.value = path
#         actions.key("enter")

#     def file_manager_select_directory(path: str):
#         """selects the directory"""
#         actions.insert(path)

#     def file_manager_new_folder(name: str):
#         """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
#         actions.key("home")
#         actions.key("ctrl-shift-n")
#         actions.insert(name)

#     def file_manager_open_file(path: str):
#         """opens the file"""
#         actions.key("ctrl-l")
#         toolbar = ui.active_window().element.find_one(automation_id = "TextBox", max_depth=0)
#         toolbar.value_pattern.value = path
#         actions.key("enter")

#     def file_manager_select_file(path: str):
#         """selects the file"""
#         actions.key("home")
#         actions.insert(path)

#     def file_manager_open_volume(volume: str):
#         """file_manager_open_volume"""
#         actions.user.file_manager_open_directory(volume)

#     def address_focus():
#         actions.key("ctrl-l")

#     def address_copy_address():
#         clip.set_text(get_active_explorer_path())

#     def address_navigate(address: str):
#         actions.user.file_manager_open_directory(address)
