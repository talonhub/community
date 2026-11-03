"""Which app a window belongs to, as the Windows taskbar sees it: its name and grouping.

Shared by the app switcher (the running list) and the thumbnail switcher. resolve(hwnd)
gives an AppIdentity: the name on the window's taskbar button and a key that groups
windows like taskbar buttons do. The order was checked against the taskbar for every
app in shell:AppsFolder that could be launched:

1. a display name the window sets for the taskbar (Git Bash's mintty, "Git Bash");
2. the Start menu shortcut the process was launched from, for processes without an id
   of their own (IDLE runs as pythonw.exe);
3. for host processes, what they were started for: each MMC console (mmc.exe opening
   an .msc) is an app, named like its Start menu entry or else its title; each
   rundll32 or dllhost process (Control Panel applets like "Mouse Properties", COM
   surrogates) is an app named by its window title;
4. the shell's name for the window's AppUserModelID, or its process's for packaged apps
   (PWAs like Slack, Store apps like Paint; File Explorer windows get the id
   "Microsoft.Windows.Explorer");
5. the Start menu shortcut carrying that id;
6. an override registered with register_name_override (the app switcher's
   launch_applications.json display names);
7. the Start menu name of the executable (cmd.exe is "Command Prompt");
8. the executable's FileDescription or ProductName;
9. the fallback passed in (Talon's app name), then the executable's file name.

Identities are cached per window; a new window is looked at again for a few seconds,
as browsers set a PWA window's id just after creating it.
"""

import ctypes
import os
import re
import threading
import time
from dataclasses import dataclass
from ctypes import wintypes

from talon import app

from . import shell_apps, shell_com
from .com_thread import on_com_thread

EXPLORER_ID = "Microsoft.Windows.Explorer"
# Processes hosting documents the taskbar treats as apps of their own: each MMC
# console (services.msc, eventvwr.msc) gets its own button, name and icon.
HOST_DOCUMENTS = {"mmc.exe": ".msc"}
# Generic hosts the taskbar also tells apart by their command line, naming each window by
# its title: rundll32 runs Control Panel applets ("Shell32.dll,Control_RunDLL main.cpl"
# is "Mouse Properties"), dllhost runs COM surrogates.
COMMAND_LINE_HOSTS = {"rundll32.exe", "dllhost.exe"}
# How long a new window's identity is re-read before it's cached for good.
SETTLE_SECONDS = 3.0

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
STARTF_TITLEISLINKNAME = 0x00000800
ERROR_INSUFFICIENT_BUFFER = 122

if app.platform == "windows":
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    ntdll = ctypes.WinDLL("ntdll")
    version = ctypes.WinDLL("version")
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.InternalGetWindowText.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
    kernel32.GetApplicationUserModelId.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.UINT), wintypes.LPWSTR]
    kernel32.ReadProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    version.GetFileVersionInfoSizeW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
    version.GetFileVersionInfoW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p]
    version.VerQueryValueW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.UINT)]


@dataclass(frozen=True)
class AppIdentity:
    # Windows with the same key share a taskbar button: the owning executable, split by
    # AppUserModelID (PWAs, apps hosted by ApplicationFrameHost) or by the document a
    # host process opened (MMC consoles).
    key: tuple[str, str]
    # The name on the taskbar button.
    name: str
    exe_path: str
    # The owning executable's file name, lowercase.
    process: str
    # The window's own AppUserModelID, and its process's if it is a packaged app.
    window_id: str | None
    process_id: str | None
    # For host processes: the document opened (an MMC console's .msc), and its Apps
    # folder id ("{1AC14E77-...}\services.msc") if it has one.
    document: str | None
    document_id: str | None
    # The window's own icon is the right one, the executable's isn't: hosted under
    # another app's id (a PWA inside Edge), or a Control Panel applet in rundll32.
    hosted: bool
    # A file whose shell icon is the app's icon: an MMC console's .msc. (A .cpl's shell
    # icon is the same generic one for every applet; their windows have the right one.)
    icon_source: str | None = None

    @property
    def model_id(self) -> str | None:
        """The window's own id wins (a PWA in Edge); packaged apps like Paint may only
        have the process's."""
        return self.window_id or self.process_id


# --- small Win32 helpers ---

def window_pid(hwnd: int) -> int:
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def window_class(hwnd: int) -> str:
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buf, len(buf))
    return buf.value


def window_text(hwnd: int) -> str:
    """The window's title, read without messaging it, so a hung window can't block."""
    buf = ctypes.create_unicode_buffer(512)
    user32.InternalGetWindowText(hwnd, buf, len(buf))
    return buf.value


def process_image(hwnd: int) -> str:
    """The executable of the process that owns the window, or ""."""
    process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, window_pid(hwnd))
    if not process:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = wintypes.DWORD(len(buf))
        if not kernel32.QueryFullProcessImageNameW(process, 0, buf, ctypes.byref(size)):
            return ""
        return buf.value
    finally:
        kernel32.CloseHandle(process)


def process_model_id(pid: int) -> str | None:
    """The AppUserModelID of a packaged (Store, MSIX) app's process, or None."""
    process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not process:
        return None
    try:
        # Asking for the length with a NULL buffer fails with ERROR_INVALID_PARAMETER
        # (87) on current Windows, so start with a buffer and grow it if needed.
        length = wintypes.UINT(256)
        buf = ctypes.create_unicode_buffer(length.value)
        result = kernel32.GetApplicationUserModelId(process, ctypes.byref(length), buf)
        if result == ERROR_INSUFFICIENT_BUFFER:
            buf = ctypes.create_unicode_buffer(length.value)
            result = kernel32.GetApplicationUserModelId(process, ctypes.byref(length), buf)
        # APPMODEL_ERROR_NO_APPLICATION (15703): not packaged.
        return (buf.value or None) if result == 0 else None
    finally:
        kernel32.CloseHandle(process)


def file_description(path: str) -> str | None:
    """The executable's FileDescription (what the taskbar shows for unpackaged apps),
    else its ProductName."""
    size = version.GetFileVersionInfoSizeW(path, None)
    if not size:
        return None
    data = ctypes.create_string_buffer(size)
    if not version.GetFileVersionInfoW(path, 0, size, data):
        return None
    pointer, length = ctypes.c_void_p(), wintypes.UINT()
    if not version.VerQueryValueW(data, r"\VarFileInfo\Translation", ctypes.byref(pointer), ctypes.byref(length)) or length.value < 4:
        return None
    language, codepage = ctypes.cast(pointer, ctypes.POINTER(wintypes.WORD * 2)).contents
    for field in ("FileDescription", "ProductName"):
        key = rf"\StringFileInfo\{language:04x}{codepage:04x}\{field}"
        if version.VerQueryValueW(data, key, ctypes.byref(pointer), ctypes.byref(length)) and length.value > 1:
            text = ctypes.wstring_at(pointer.value, length.value).rstrip("\0").strip()
            if text:
                return text
    return None


class PROCESS_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ExitStatus", ctypes.c_void_p),
        ("PebBaseAddress", ctypes.c_void_p),
        ("AffinityMask", ctypes.c_void_p),
        ("BasePriority", ctypes.c_void_p),
        ("UniqueProcessId", ctypes.c_void_p),
        ("InheritedFromUniqueProcessId", ctypes.c_void_p),
    ]


def _process_parameters(pid: int) -> tuple[int, str, str] | None:
    """(startup flags, startup "window title", command line) from the process's PEB,
    or None if it can't be read. 64-bit layout: ProcessParameters at +0x20; in
    RTL_USER_PROCESS_PARAMETERS, CommandLine at +0x70, WindowFlags at +0xA4 and
    WindowTitle at +0xB0."""
    process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not process:
        return None

    def read(address, size):
        buf = ctypes.create_string_buffer(size)
        done = ctypes.c_size_t()
        if not kernel32.ReadProcessMemory(process, ctypes.c_void_p(address), buf, size, ctypes.byref(done)) or done.value != size:
            return None
        return buf.raw

    def read_string(address) -> str:
        """A UNICODE_STRING: length (bytes) at +0, buffer pointer at +8."""
        raw = read(address, 16)
        if raw is None:
            return ""
        length = int.from_bytes(raw[0:2], "little")
        buffer = int.from_bytes(raw[8:16], "little")
        text = read(buffer, length) if length and buffer else None
        return text.decode("utf-16-le", "replace") if text else ""

    try:
        info = PROCESS_BASIC_INFORMATION()
        if ntdll.NtQueryInformationProcess(process, 0, ctypes.byref(info), ctypes.sizeof(info), None) != 0 or not info.PebBaseAddress:
            return None
        raw = read(info.PebBaseAddress + 0x20, 8)
        if raw is None:
            return None
        params = int.from_bytes(raw, "little")
        raw = read(params + 0xA4, 4)
        if raw is None:
            return None
        return int.from_bytes(raw, "little"), read_string(params + 0xB0), read_string(params + 0x70)
    finally:
        kernel32.CloseHandle(process)


def process_launch_shortcut(pid: int) -> str | None:
    """The .lnk a process was started from, if the shell started it from a shortcut.

    The shell passes the shortcut's path as the startup "window title" with
    STARTF_TITLEISLINKNAME set; the taskbar names such a process after the shortcut
    ("IDLE (Python 3.12 ARM64)" for pythonw.exe).
    """
    parameters = _process_parameters(pid)
    if parameters is None or not parameters[0] & STARTF_TITLEISLINKNAME:
        return None
    title = parameters[1]
    return title if title.lower().endswith(".lnk") else None


def host_document(pid: int, exe_name: str) -> str | None:
    """For a host process like mmc.exe, the document it opened (from its command line)."""
    extension = HOST_DOCUMENTS.get(exe_name.lower())
    if not extension:
        return None
    parameters = _process_parameters(pid)
    if parameters is None:
        return None
    ext = re.escape(extension)
    match = re.search(rf'"([^"]+{ext})"|(\S+{ext})\b', parameters[2], re.IGNORECASE)
    return (match.group(1) or match.group(2)) if match else None


def host_command(pid: int) -> str | None:
    """A process's command line without its executable, e.g.
    "Shell32.dll,Control_RunDLL main.cpl" for a rundll32 running the Mouse applet."""
    parameters = _process_parameters(pid)
    if parameters is None:
        return None
    line = parameters[2].strip()
    if line.startswith('"'):
        rest = line[line.find('"', 1) + 1 :] if line.find('"', 1) > 0 else ""
    else:
        rest = line.split(None, 1)[1] if len(line.split(None, 1)) > 1 else ""
    return rest.strip() or None


def shortcut_name(path: str) -> str:
    """A shortcut's name as the shell (and the taskbar) shows it: localized, e.g.
    "Services" for Administrative Tools' services.lnk. COM: call on the COM thread."""
    item = shell_com.create_item(path)
    if item is not None:
        try:
            name = shell_com.item_name(item)
        finally:
            shell_com.release(item)
        if name:
            return name
    return os.path.splitext(os.path.basename(path))[0]


def console_name(title: str) -> str:
    """An MMC console's name from its title, without author mode's " - [Console Root]"."""
    return title.split(" - [")[0].strip()


# --- names ---

# Overrides by AppUserModelID; see register_name_override.
_name_override = None
# Taskbar names by (AppUserModelID, executable path), lowercase; "" when unknown.
_app_names: dict[tuple[str, str], str] = {}


def register_name_override(lookup):
    """Let `lookup(app_user_model_id) -> name | None` name apps whose id the shell has no
    name for (the app switcher registers launch_applications.json's display names)."""
    global _name_override
    _name_override = lookup
    clear_names()


def clear_names():
    """Forget cached names and identities, e.g. after the overrides changed."""
    _app_names.clear()
    with _lock:
        _cache.clear()


@on_com_thread
def window_relaunch_name(hwnd: int) -> str | None:
    """The display name a window asks the taskbar to use (its relaunch display name),
    e.g. "Git Bash" for Git Bash's mintty window; "@file,-id" resources resolved."""
    text = shell_com.resolve_indirect(shell_com.window_property(hwnd, shell_com.PKEY_AppUserModel_RelaunchDisplayNameResource))
    return text.strip() if text and text.strip() else None


@on_com_thread
def window_model_id(hwnd: int) -> str | None:
    """The window's own AppUserModelID, if it sets one."""
    return shell_com.window_property(hwnd, shell_com.PKEY_AppUserModel_ID)


@on_com_thread
def display_name(model_id: str | None, path: str, fallback: str) -> str:
    """The name the taskbar shows for an app by its AppUserModelID and executable
    (steps 4 to 9 in the module docstring). Cached."""
    key = ((model_id or "").lower(), (path or "").lower())
    if key not in _app_names:
        name = None
        if model_id:
            item = shell_com.create_item(f"shell:AppsFolder\\{model_id}")
            if item is not None:
                try:
                    name = shell_com.item_name(item)
                finally:
                    shell_com.release(item)
        if not name and model_id:
            name = shell_apps.shortcut_names_by_id().get(model_id.lower())
        if not name and model_id and _name_override is not None:
            try:
                name = _name_override(model_id)
            except Exception:
                name = None
        if not name and path:
            name = shell_apps.name_for_path(path)
        if not name and path:
            try:
                name = file_description(path)
            except OSError:
                name = None
        _app_names[key] = name or ""
    if _app_names[key]:
        return _app_names[key]
    return fallback or os.path.splitext(os.path.basename(path or ""))[0]


@on_com_thread
def _resolve(hwnd: int, fallback: str) -> AppIdentity:
    """All of resolve() in one trip to the COM thread."""
    path = process_image(hwnd)
    process = os.path.basename(path).lower()
    pid = window_pid(hwnd)
    window_id = shell_com.window_property(hwnd, shell_com.PKEY_AppUserModel_ID)
    if not window_id and process == "explorer.exe" and window_class(hwnd) == "CabinetWClass":
        # File Explorer windows don't set an id; the shell groups them under this one.
        window_id = EXPLORER_ID
    process_id = process_model_id(pid)
    relaunch_name = window_relaunch_name(hwnd)
    if not relaunch_name and not window_id and not process_id:
        shortcut = process_launch_shortcut(pid)
        if shortcut:
            relaunch_name = shortcut_name(shortcut)
    model_id = window_id or process_id
    name = relaunch_name or display_name(model_id, path, fallback)
    hosted = bool(window_id) and name != display_name(None, path, fallback)
    document = document_id = icon_source = None
    if not window_id:
        document = host_document(pid, process)
        if document:
            document_id = shell_apps.app_id_for_path(document)
            name = relaunch_name or shell_apps.name_for_path(document) or console_name(window_text(hwnd)) or name
            icon_source = document
        elif process in HOST_DOCUMENTS:
            # A console without a document (mmc.exe alone): the taskbar uses its title,
            # e.g. "Console1".
            name = relaunch_name or console_name(window_text(hwnd)) or name
        elif process in COMMAND_LINE_HOSTS:
            document = host_command(pid)
            if document:
                name = relaunch_name or window_text(hwnd).strip() or name
                hosted = True
    key = (process or fallback.lower(), (model_id or document or "").lower())
    return AppIdentity(key, name, path, process, window_id, process_id, document, document_id, hosted, icon_source)


_lock = threading.Lock()
# hwnd -> (pid, when first seen, identity)
_cache: dict[int, tuple[int, float, AppIdentity]] = {}


def resolve(hwnd: int, fallback: str = "") -> AppIdentity:
    """The window's app as the taskbar sees it; `fallback` (Talon's app name) names apps
    nothing else names. Cached per window once it has settled."""
    now = time.monotonic()
    pid = window_pid(hwnd)
    with _lock:
        cached = _cache.get(hwnd)
    if cached is not None and cached[0] == pid and now - cached[1] >= SETTLE_SECONDS:
        return cached[2]
    identity = _resolve(hwnd, fallback)
    with _lock:
        first_seen = cached[1] if cached is not None and cached[0] == pid else now
        _cache[hwnd] = (pid, first_seen, identity)
    return identity


def forget_others(live_hwnds):
    """Drop cached identities of windows not in `live_hwnds` (closed windows)."""
    live = set(live_hwnds)
    with _lock:
        for hwnd in [h for h in _cache if h not in live]:
            del _cache[hwnd]
