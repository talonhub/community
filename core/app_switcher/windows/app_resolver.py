"""The AppUserModelID the taskbar uses for a window or process, from the shell itself.

Explorer resolves taskbar ids with IApplicationResolver, created from
CLSID_StartMenuCacheAndAppResolver. It combines a window's and a process's explicit
ids, Start menu shortcut matching, packaged apps and the computed fallback (for
example "{1AC14E77-...}\\cmd.exe"), so it is the only way to get the taskbar's answer
in every case. Tools like 7+ Taskbar Tweaker and Windhawk mods use it.

The interface is undocumented. Its id changed between Windows 7 and 8; the Windows 8+
id and vtable layout below were checked on Windows 11 build 26300. If the interface
isn't available, the functions return None and callers fall back to documented APIs.

Runs on the shared COM thread (see com_thread.py). The resolver is an in-process
server, so calls don't wait on Explorer.
"""

import ctypes
from ctypes import wintypes

from .com_thread import on_com_thread
from .shell_com import GUID, HRESULT, PTR, _take_string, call, ole32, ref

CLSID_StartMenuCacheAndAppResolver = "{660B90C8-73A9-4B58-8CAE-355B7F55341B}"
# Windows 8 and later. (Windows 7's {46A6EEFF-908E-4DC6-92A6-64BE9177B41C} has a
# different layout and isn't supported.)
IID_IApplicationResolver = "{DE25675A-72DE-44B4-9373-05170450C140}"
CLSCTX_INPROC_SERVER = 0x1

# Vtable slots after IUnknown: GetAppIDForShortcut (3), GetAppIDForShortcutObject (4),
# then these two, which share a signature:
#   HRESULT (HWND or DWORD pid, LPWSTR *app_id, BOOL *pinning_prevented,
#            BOOL *explicit_app_id, BOOL *embedded_shortcut_valid)
GET_APP_ID_FOR_WINDOW = 5
GET_APP_ID_FOR_PROCESS = 6

# None until first used; False if the interface isn't available on this Windows.
_resolver = None


def _get_resolver():
    global _resolver
    if _resolver is None:
        out = PTR()
        hr = ole32.CoCreateInstance(
            ref(GUID(CLSID_StartMenuCacheAndAppResolver)),
            None,
            CLSCTX_INPROC_SERVER,
            ref(GUID(IID_IApplicationResolver)),
            ref(out),
        )
        if hr != 0 or not out:
            print(f"app_resolver: IApplicationResolver unavailable: 0x{hr & 0xFFFFFFFF:08x}")
        _resolver = out if hr == 0 and out else False
    return _resolver or None


def _app_id(slot: int, arg) -> str | None:
    resolver = _get_resolver()
    if resolver is None:
        return None
    app_id = ctypes.c_wchar_p()
    pinning_prevented, explicit, embedded = wintypes.BOOL(), wintypes.BOOL(), wintypes.BOOL()
    hr = call(resolver, slot, HRESULT, arg, ref(app_id), ref(pinning_prevented), ref(explicit), ref(embedded))
    if hr != 0:
        return None
    return _take_string(app_id)


def available() -> bool:
    """Whether IApplicationResolver could be created on this Windows."""
    return _on_thread_available()


@on_com_thread
def _on_thread_available() -> bool:
    return _get_resolver() is not None


@on_com_thread
def window_app_id(hwnd: int) -> str | None:
    """The id the taskbar groups this window under (e.g. Microsoft.Windows.Explorer for
    File Explorer, Microsoft.Windows.ControlPanel for Control Panel), or None."""
    return _app_id(GET_APP_ID_FOR_WINDOW, wintypes.HWND(hwnd))


@on_com_thread
def process_app_id(pid: int) -> str | None:
    """The id the shell gives this process as a whole, or None. Hosts report themselves:
    Settings' frame window resolves to its app, its ApplicationFrameHost process to
    the host."""
    return _app_id(GET_APP_ID_FOR_PROCESS, wintypes.DWORD(pid))
