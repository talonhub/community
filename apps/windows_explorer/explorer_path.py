"""Read the filesystem path of the active File Explorer window.

pywin32 (win32com / win32gui) has no free-threaded build, so instead of
Shell.Application late binding we drive the Shell COM interfaces directly
through ctypes. This works with or without the GIL and has no third-party
dependency.

The public entry point is get_active_explorer_path
"""

from talon import app, ui


class ExplorerPath(str):
    """The active Explorer location, as a str with an origin flag.

    For ordinary folders the value is the filesystem path and
    is_virtual is false. For virtual folders that have no
    filesystem path the value is the shell parsing name (e.g.
    ::{20D04FE0-3AEA-1069-A2D8-08002B30309D} for This PC).
    """

    is_virtual: bool

    def __new__(cls, value: str, *, is_virtual: bool):
        obj = super().__new__(cls, value)
        obj.is_virtual = is_virtual
        return obj

if app.platform == "windows":
    import ctypes
    from ctypes import POINTER, byref, c_void_p, c_long, c_ulong, c_longlong, c_ushort
    from ctypes import wintypes

    # ---- Minimal ctypes COM plumbing (free-threaded compatible) ------------
    S_OK = 0
    S_FALSE = 1
    RPC_E_CHANGED_MODE = -2147417850  # 0x80010106
    COINIT_APARTMENTTHREADED = 0x2
    CLSCTX_ALL = 0x17
    VT_I4 = 3
    GA_ROOT = 2
    # SIGDN flags for SHGetNameFromIDList. FILESYSPATH yields the filesystem
    # path and succeeds only for filesystem-backed items; DESKTOPABSOLUTEPARSING
    # yields the canonical, locale-independent parsing name (a form like
    # "::{CLSID}" for virtual folders, which the address bar accepts).
    # Neither is capped at MAX_PATH -- the shell allocates the buffer -- so
    # unlike the legacy SHGetPathFromIDListW they handle long (>260) paths.
    SIGDN_FILESYSPATH = 0x80058000
    SIGDN_DESKTOPABSOLUTEPARSING = 0x80028000

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", ctypes.c_uint32),
            ("Data2", ctypes.c_uint16),
            ("Data3", ctypes.c_uint16),
            ("Data4", ctypes.c_ubyte * 8),
        ]

    # 64-bit VARIANT is 24 bytes; padded so it is passed by value correctly.
    class VARIANT(ctypes.Structure):
        _fields_ = [
            ("vt", c_ushort),
            ("wReserved1", c_ushort),
            ("wReserved2", c_ushort),
            ("wReserved3", c_ushort),
            ("val", c_longlong),
            ("pad", c_longlong),
        ]

    _ole32 = ctypes.WinDLL("ole32")
    _shell32 = ctypes.WinDLL("shell32")
    _user32 = ctypes.WinDLL("user32")

    _ole32.CoCreateInstance.argtypes = [
        POINTER(GUID), c_void_p, wintypes.DWORD, POINTER(GUID), POINTER(c_void_p)
    ]
    _ole32.CoCreateInstance.restype = c_long
    _ole32.IIDFromString.argtypes = [ctypes.c_wchar_p, POINTER(GUID)]
    _ole32.IIDFromString.restype = c_long
    # SHGetNameFromIDList has no A/W suffix (it only ever returns a wide
    # string). It is used in place of the MAX_PATH-bound SHGetPathFromIDListW
    # so that long filesystem paths are not truncated.
    _shell32.SHGetNameFromIDList.argtypes = [
        c_void_p, wintypes.DWORD, POINTER(c_void_p)
    ]
    _shell32.SHGetNameFromIDList.restype = c_long
    _user32.GetForegroundWindow.restype = wintypes.HWND
    _user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
    _user32.GetAncestor.restype = wintypes.HWND
    _user32.FindWindowExW.argtypes = [
        wintypes.HWND, wintypes.HWND, ctypes.c_wchar_p, ctypes.c_wchar_p
    ]
    _user32.FindWindowExW.restype = wintypes.HWND

    def _guid(s: str) -> GUID:
        g = GUID()
        if _ole32.IIDFromString(s, byref(g)) != S_OK:
            raise OSError(f"IIDFromString failed for {s}")
        return g

    CLSID_ShellWindows = _guid("{9BA05972-F6A8-11CF-A442-00A0C90A8F39}")
    IID_IShellWindows = _guid("{85CB6900-4D95-11CF-960C-0080C7F4EE85}")
    IID_IServiceProvider = _guid("{6D5140C1-7436-11CE-8034-00AA006009FA}")
    SID_STopLevelBrowser = _guid("{4C96BE40-915C-11CF-99D3-00AA004AE837}")
    IID_IShellBrowser = _guid("{000214E2-0000-0000-C000-000000000046}")
    # SID_SShellBrowser is the same GUID as IID_IShellBrowser. Asking the
    # service provider for this service returns the browser for *this* tab,
    # whereas SID_STopLevelBrowser returns a single browser shared by every
    # tab in the window (and so cannot distinguish the active tab).
    SID_SShellBrowser = IID_IShellBrowser
    # Win11 Explorer hosts each tab in a child window of this class; the
    # active tab is the topmost one in z-order.
    SHELL_TAB_WINDOW_CLASS = "ShellTabWindowClass"
    IID_IFolderView = _guid("{CDE725B0-CCC9-4519-917E-325D72FAB4CE}")
    IID_IPersistFolder2 = _guid("{1AC3D9F0-175C-11D1-95BE-00609797EA4F}")

    def _vtable_call(this, index, restype, *args):
        """Call the vtable method at index on a raw COM interface pointer.

        Each entry in args is a (ctype, value) tuple for that argument.
        """
        vtbl = ctypes.cast(this, POINTER(c_void_p))[0]
        fn_addr = ctypes.cast(vtbl, POINTER(c_void_p))[index]
        proto = ctypes.WINFUNCTYPE(restype, c_void_p, *[a[0] for a in args])
        return proto(fn_addr)(this, *[a[1] for a in args])

    def _release(ptr):
        if ptr:
            _vtable_call(ptr, 2, c_ulong)

    def _location_from_pidl(pidl):
        """Resolve an absolute PIDL to an ExplorerPath, or None.

        SIGDN_FILESYSPATH succeeds only for filesystem-backed items and,
        because the shell allocates the string, is not capped at MAX_PATH, so
        long (>260) paths come back intact and is_virtual is False.
        Virtual folders (This PC, Home, Network, Recycle Bin, ...) fail that
        and fall back to the canonical parsing name (is_virtual True).
        Returns None if neither can be obtained.
        """
        for sigdn, is_virtual in (
            (SIGDN_FILESYSPATH, False),
            (SIGDN_DESKTOPABSOLUTEPARSING, True),
        ):
            name = c_void_p()
            if _shell32.SHGetNameFromIDList(pidl, sigdn, byref(name)) == S_OK and name:
                try:
                    value = ctypes.wstring_at(name)
                finally:
                    _ole32.CoTaskMemFree(name)
                if value:
                    return ExplorerPath(value, is_virtual=is_virtual)
        return None

    def _path_from_browser(disp, hwnd_fg, active_tab):
        # IUnknown::QueryInterface for IServiceProvider
        sp = c_void_p()
        if _vtable_call(disp, 0, c_long,
                        (POINTER(GUID), byref(IID_IServiceProvider)),
                        (POINTER(c_void_p), byref(sp))) != S_OK or not sp:
            return None
        try:
            # IServiceProvider::QueryService(SID_SShellBrowser) -> the
            # IShellBrowser for this specific tab.
            sb = c_void_p()
            if _vtable_call(sp, 3, c_long,
                            (POINTER(GUID), byref(SID_SShellBrowser)),
                            (POINTER(GUID), byref(IID_IShellBrowser)),
                            (POINTER(c_void_p), byref(sb))) != S_OK or not sb:
                return None
            try:
                # IOleWindow::GetWindow -> this tab's window handle.
                hwnd = wintypes.HWND()
                if _vtable_call(sb, 3, c_long,
                                (POINTER(wintypes.HWND), byref(hwnd))) != S_OK:
                    return None
                if active_tab:
                    # Window has tabs: match the active tab exactly.
                    if hwnd.value != active_tab:
                        return None
                elif _user32.GetAncestor(hwnd, GA_ROOT) != hwnd_fg:
                    # No tab handle available: fall back to matching the
                    # owning top-level window.
                    return None

                # IShellBrowser::QueryActiveShellView -> IShellView
                sv = c_void_p()
                if _vtable_call(sb, 15, c_long,
                                (POINTER(c_void_p), byref(sv))) != S_OK or not sv:
                    return None
                try:
                    # IShellView -> IFolderView
                    fv = c_void_p()
                    if _vtable_call(sv, 0, c_long,
                                    (POINTER(GUID), byref(IID_IFolderView)),
                                    (POINTER(c_void_p), byref(fv))) != S_OK or not fv:
                        return None
                    try:
                        # IFolderView::GetFolder -> IPersistFolder2
                        pf2 = c_void_p()
                        if _vtable_call(fv, 5, c_long,
                                        (POINTER(GUID), byref(IID_IPersistFolder2)),
                                        (POINTER(c_void_p), byref(pf2))) != S_OK or not pf2:
                            return None
                        try:
                            # IPersistFolder2::GetCurFolder -> PIDL
                            pidl = c_void_p()
                            if _vtable_call(pf2, 5, c_long,
                                            (POINTER(c_void_p), byref(pidl))) != S_OK or not pidl:
                                return None
                            try:
                                return _location_from_pidl(pidl)
                            finally:
                                _ole32.CoTaskMemFree(pidl)
                        finally:
                            _release(pf2)
                    finally:
                        _release(fv)
                finally:
                    _release(sv)
            finally:
                _release(sb)
        finally:
            _release(sp)

    def _get_active_explorer_path_windows():
        hwnd_fg = ui.active_window().id
        if not hwnd_fg:
            return None

        # The active tab is hosted in the topmost ShellTabWindowClass child
        # of the foreground window. FindWindowEx enumerates children in
        # z-order, so the first match is the active tab. Returns 0 when the
        # window has no such child (e.g. older Explorer without tabs).
        active_tab = _user32.FindWindowExW(
            hwnd_fg, None, SHELL_TAB_WINDOW_CLASS, None
        )

        hr = _ole32.CoInitializeEx(None, COINIT_APARTMENTTHREADED)
        need_uninit = hr in (S_OK, S_FALSE)
        try:
            shell_windows = c_void_p()
            if _ole32.CoCreateInstance(
                byref(CLSID_ShellWindows), None, CLSCTX_ALL,
                byref(IID_IShellWindows), byref(shell_windows),
            ) != S_OK or not shell_windows:
                return None
            try:
                # IShellWindows::get_Count
                count = c_long(0)
                if _vtable_call(shell_windows, 7, c_long,
                                (POINTER(c_long), byref(count))) != S_OK:
                    return None
                for i in range(count.value):
                    # IShellWindows::Item(VARIANT index) -> IDispatch
                    var = VARIANT()
                    var.vt = VT_I4
                    var.val = i
                    disp = c_void_p()
                    if _vtable_call(shell_windows, 8, c_long,
                                    (VARIANT, var),
                                    (POINTER(c_void_p), byref(disp))) != S_OK or not disp:
                        continue
                    try:
                        path = _path_from_browser(disp, hwnd_fg, active_tab)
                        if path is not None:
                            return path
                    finally:
                        _release(disp)
                return None
            finally:
                _release(shell_windows)
        finally:
            if need_uninit:
                _ole32.CoUninitialize()


def get_active_explorer_path():
    """Return the active Explorer window's location, or None.

    The result is an ExplorerPath (a str): a filesystem path for
    ordinary folders, or a shell parsing name for virtual folders such as
    This PC or Home. Check .is_virtual to tell them apart. 
    """
    if app.platform != "windows":
        return None
    return _get_active_explorer_path_windows()
