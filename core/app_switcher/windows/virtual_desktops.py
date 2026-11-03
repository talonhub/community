"""Windows virtual desktops through COM, with plain ctypes.

Which desktop a window is on comes from the documented IVirtualDesktopManager, which
works for any window. Listing, naming, switching, creating and removing desktops, and
moving other processes' windows between them, need the undocumented
IVirtualDesktopManagerInternal and IApplicationViewCollection interfaces of the shell.
Their GUIDs and method order change between Windows builds; these follow pyvda
(https://github.com/mirober/pyvda), and only the newest layout (build 26100 and later)
is implemented. On other builds, or if the shell refuses, `available()` is False and
only the documented parts work. Every call runs on the switcher's own COM thread.
"""

import ctypes
import threading
import winreg
from ctypes import wintypes

from talon import app

from .com_thread import on_com_thread

CLSCTX_ALL = 0x17
MIN_BUILD = 26100


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]

    @classmethod
    def parse(cls, text: str) -> "GUID":
        guid = cls()
        ctypes.oledll.ole32.CLSIDFromString(text, ref(guid))
        return guid

    def key(self) -> bytes:
        return bytes(self)

    def __str__(self) -> str:
        d4 = bytes(self.Data4)
        return f"{self.Data1:08x}-{self.Data2:04x}-{self.Data3:04x}-{d4[:2].hex()}-{d4[2:].hex()}"


CLSID_ImmersiveShell = "{C2F03A33-21F5-47FA-B4BB-156362A2F239}"
CLSID_VirtualDesktopManagerInternal = "{C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B}"
CLSID_VirtualDesktopManager = "{AA509086-5CA9-4C25-8F95-589D3C07B48A}"
IID_IServiceProvider = "{6D5140C1-7436-11CE-8034-00AA006009FA}"
IID_IVirtualDesktopManager = "{A5CD92FF-29BE-454C-8D04-D82879FB3F1B}"
IID_IApplicationViewCollection = "{1841C6D7-4F9D-42C0-AF41-8747538F10E5}"
IID_IObjectArray = "{92CA9DCD-5622-4BBA-A805-5E9F541BD8C9}"
# Build 26100 and later, as in pyvda's const.py.
IID_IVirtualDesktop = "{3F07F4BE-B107-441A-AF0F-39D82529072C}"
IID_IVirtualDesktopManagerInternal = "{53F5CA0B-158F-4124-900C-057158060B27}"

HRESULT = ctypes.c_long
PTR = ctypes.c_void_p

# Vtable slots (IUnknown takes 0-2), in pyvda's com_defns.py order for 26100+.
RELEASE = 2
SP_QUERY_SERVICE = 3
VDM_IS_ON_CURRENT = 3
VDM_GET_DESKTOP_ID = 4
OA_GET_COUNT = 3
OA_GET_AT = 4
VD_GET_ID = 4
VD_GET_NAME = 5
VDMI_GET_COUNT = 3
VDMI_MOVE_VIEW = 4
VDMI_GET_CURRENT = 6
VDMI_GET_DESKTOPS = 7
VDMI_SWITCH = 9
VDMI_CREATE = 11
VDMI_REMOVE = 13
VDMI_FIND = 14
AVC_GET_VIEW_FOR_HWND = 6

_local = threading.local()


def windows_build() -> int:
    """The real build number; sys.getwindowsversion() says 9200 in an unmanifested exe."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
            return int(winreg.QueryValueEx(key, "CurrentBuild")[0])
    except OSError:
        return 0


def ref(value) -> PTR:
    """A pointer to a ctypes value, typed as void* so it can be a declared argument."""
    return ctypes.cast(ctypes.pointer(value), PTR)


def _call(obj, slot: int, restype, *args):
    """Call vtable `slot` of the COM interface pointer `obj` with ctypes args."""
    vtable = ctypes.cast(ctypes.cast(obj, ctypes.POINTER(PTR))[0], ctypes.POINTER(PTR))
    proto = ctypes.WINFUNCTYPE(restype, PTR, *[type(a) for a in args])
    return proto(vtable[slot])(obj, *args)


def _release(obj):
    if obj:
        _call(obj, RELEASE, wintypes.ULONG)


class _Interfaces:
    """The shell's COM objects, created on the COM thread (pointers are apartment-bound)."""

    def __init__(self):
        ole32 = ctypes.windll.ole32
        self.manager = PTR()
        hr = ole32.CoCreateInstance(
            ref(GUID.parse(CLSID_VirtualDesktopManager)),
            None,
            CLSCTX_ALL,
            ref(GUID.parse(IID_IVirtualDesktopManager)),
            ref(self.manager),
        )
        if hr != 0:
            raise OSError(f"IVirtualDesktopManager: 0x{hr & 0xFFFFFFFF:08x}")
        self.internal = PTR()
        self.views = PTR()
        self.error = None
        if windows_build() < MIN_BUILD:
            self.error = f"Windows build {windows_build()} is not supported"
            return
        shell = PTR()
        hr = ole32.CoCreateInstance(
            ref(GUID.parse(CLSID_ImmersiveShell)),
            None,
            CLSCTX_ALL,
            ref(GUID.parse(IID_IServiceProvider)),
            ref(shell),
        )
        if hr != 0:
            self.error = f"ImmersiveShell: 0x{hr & 0xFFFFFFFF:08x}"
            return
        try:
            for service, iid, out in (
                (CLSID_VirtualDesktopManagerInternal, IID_IVirtualDesktopManagerInternal, self.internal),
                (IID_IApplicationViewCollection, IID_IApplicationViewCollection, self.views),
            ):
                hr = _call(
                    shell,
                    SP_QUERY_SERVICE,
                    HRESULT,
                    ref(GUID.parse(service)),
                    ref(GUID.parse(iid)),
                    ref(out),
                )
                if hr != 0:
                    self.error = f"QueryService {iid}: 0x{hr & 0xFFFFFFFF:08x}"
                    return
        finally:
            _release(shell)


def _interfaces() -> _Interfaces:
    if getattr(_local, "interfaces", None) is None:
        _local.interfaces = _Interfaces()
    return _local.interfaces


@on_com_thread
def reset():
    """Forget the COM objects, e.g. after explorer restarted."""
    _local.interfaces = None


@on_com_thread
def available() -> bool:
    """Whether the undocumented parts (moving, switching, listing) work here."""
    try:
        return _interfaces().error is None
    except OSError:
        return False


@on_com_thread
def unavailable_reason() -> str | None:
    try:
        return _interfaces().error
    except OSError as e:
        return str(e)


# --- documented: which desktop a window is on ---


@on_com_thread
def window_desktop(hwnd: int) -> GUID | None:
    """The id of the desktop the window is on, or None (e.g. pinned or not a desktop window)."""
    try:
        manager = _interfaces().manager
    except OSError:
        return None
    guid = GUID()
    hr = _call(manager, VDM_GET_DESKTOP_ID, HRESULT, wintypes.HWND(hwnd), ref(guid))
    if hr != 0 or not any(bytes(guid)):
        return None
    return guid


@on_com_thread
def is_on_current_desktop(hwnd: int) -> bool:
    try:
        manager = _interfaces().manager
    except OSError:
        return True
    result = wintypes.BOOL()
    hr = _call(manager, VDM_IS_ON_CURRENT, HRESULT, wintypes.HWND(hwnd), ref(result))
    return hr != 0 or bool(result.value)


# --- undocumented: desktops ---


class Desktop:
    def __init__(self, number: int, guid: GUID, name: str):
        self.number = number  # 1-based, in the order Task View shows them
        self.guid = guid
        self.name = name

    def label(self) -> str:
        return f"{self.number}: {self.name}" if self.name else f"Desktop {self.number}"


def _hstring(handle) -> str:
    if not handle:
        return ""
    length = wintypes.UINT()
    combase = ctypes.windll.combase
    combase.WindowsGetStringRawBuffer.restype = wintypes.LPCWSTR
    text = combase.WindowsGetStringRawBuffer(handle, ref(length)) or ""
    combase.WindowsDeleteString(handle)
    return text


def _desktop_objects() -> list:
    """IVirtualDesktop pointers in order; the caller releases them."""
    internal = _interfaces().internal
    array = PTR()
    if _call(internal, VDMI_GET_DESKTOPS, HRESULT, ref(array)) != 0:
        return []
    try:
        count = wintypes.UINT()
        _call(array, OA_GET_COUNT, HRESULT, ref(count))
        iid = GUID.parse(IID_IVirtualDesktop)
        desktops = []
        for i in range(count.value):
            desktop = PTR()
            if _call(array, OA_GET_AT, HRESULT, wintypes.UINT(i), ref(iid), ref(desktop)) == 0:
                desktops.append(desktop)
        return desktops
    finally:
        _release(array)


def _desktop_info(number: int, desktop) -> Desktop:
    guid = GUID()
    _call(desktop, VD_GET_ID, HRESULT, ref(guid))
    name = PTR()
    _call(desktop, VD_GET_NAME, HRESULT, ref(name))
    return Desktop(number, guid, _hstring(name))


@on_com_thread
def desktops() -> list[Desktop]:
    """All desktops in Task View order; empty when unavailable."""
    if not available():
        return []
    objects = _desktop_objects()
    try:
        return [_desktop_info(i + 1, d) for i, d in enumerate(objects)]
    finally:
        for d in objects:
            _release(d)


@on_com_thread
def current_desktop() -> Desktop | None:
    if not available():
        return None
    internal = _interfaces().internal
    desktop = PTR()
    if _call(internal, VDMI_GET_CURRENT, HRESULT, ref(desktop)) != 0:
        return None
    try:
        info = _desktop_info(0, desktop)
    finally:
        _release(desktop)
    for d in desktops():
        if d.guid.key() == info.guid.key():
            return d
    return None


def _find(guid: GUID):
    desktop = PTR()
    if _call(_interfaces().internal, VDMI_FIND, HRESULT, ref(guid), ref(desktop)) != 0:
        raise OSError(f"no desktop {guid}")
    return desktop


@on_com_thread
def switch_to(guid: GUID):
    desktop = _find(guid)
    try:
        hr = _call(_interfaces().internal, VDMI_SWITCH, HRESULT, desktop)
    finally:
        _release(desktop)
    if hr != 0:
        raise OSError(f"SwitchDesktop: 0x{hr & 0xFFFFFFFF:08x}")


@on_com_thread
def move_window(hwnd: int, guid: GUID):
    """Move any process's window to the desktop `guid`, through its application view."""
    interfaces = _interfaces()
    view = PTR()
    hr = _call(interfaces.views, AVC_GET_VIEW_FOR_HWND, HRESULT, wintypes.HWND(hwnd), ref(view))
    if hr != 0 or not view:
        raise OSError(f"GetViewForHwnd: 0x{hr & 0xFFFFFFFF:08x}")
    desktop = PTR()
    try:
        desktop = _find(guid)
        hr = _call(interfaces.internal, VDMI_MOVE_VIEW, HRESULT, view, desktop)
        if hr != 0:
            raise OSError(f"MoveViewToDesktop: 0x{hr & 0xFFFFFFFF:08x}")
    finally:
        _release(desktop)
        _release(view)


@on_com_thread
def create_desktop() -> Desktop:
    desktop = PTR()
    hr = _call(_interfaces().internal, VDMI_CREATE, HRESULT, ref(desktop))
    if hr != 0:
        raise OSError(f"CreateDesktop: 0x{hr & 0xFFFFFFFF:08x}")
    try:
        guid = _desktop_info(0, desktop).guid
    finally:
        _release(desktop)
    return next(d for d in desktops() if d.guid.key() == guid.key())


@on_com_thread
def remove_desktop(guid: GUID, fallback: GUID):
    """Remove a desktop; its windows go to `fallback`."""
    desktop = _find(guid)
    other = PTR()
    try:
        other = _find(fallback)
        hr = _call(_interfaces().internal, VDMI_REMOVE, HRESULT, desktop, other)
        if hr != 0:
            raise OSError(f"RemoveDesktop: 0x{hr & 0xFFFFFFFF:08x}")
    finally:
        _release(desktop)
        _release(other)


if app.platform != "windows":

    def available() -> bool:  # noqa: F811
        return False
