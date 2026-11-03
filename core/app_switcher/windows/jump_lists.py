"""Apps' jump lists, as the Start menu and taskbar show them: tasks, custom categories
(VS Code's "Recent Folders", Edge's "Top Sites") and recent / frequent items.

- Tasks and custom categories are in
  %APPDATA%\\Microsoft\\Windows\\Recent\\CustomDestinations\\<hash>.customDestinations-ms.
  No API reads another app's list, so the file is parsed: a header, then categories of
  serialized ShellLink objects, each loaded with IPersistStream.
- Recent items come from IApplicationDocumentLists.
- Pinned items, pinning, unpinning and removing items go through the shell's own
  IAutomaticDestinationList (undocumented; the interface Explorer uses for the taskbar's
  jump lists, IAutomaticDestinationList10b on Windows 10 and 11), so changes show up in
  the taskbar's and Start's jump lists. Without it (another Windows version), pinned
  items aren't shown and only removing is offered.

<hash> is a CRC-64 of the app's AppUserModelID in uppercase UTF-16. Everything runs on
the shared COM thread; lists are cached by the files' modification time.
"""

import ctypes
import glob
import os
import struct
import time
from dataclasses import dataclass, field
from ctypes import wintypes

from talon import app

from . import shell_com
from .com_thread import on_com_thread
from .shell_com import GUID, HRESULT, PTR, call, ref, release

DESTINATIONS = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Recent")
CUSTOM_DIR = os.path.join(DESTINATIONS, "CustomDestinations")
AUTOMATIC_DIR = os.path.join(DESTINATIONS, "AutomaticDestinations")
FOOTER = 0xBABFFBAB
CATEGORY_CUSTOM, CATEGORY_KNOWN, CATEGORY_TASKS = 0, 1, 2
KDC_FREQUENT, KDC_RECENT = 1, 2
ADLT_RECENT, ADLT_FREQUENT = 0, 1
RECENT_ITEMS = 10
# How long recent items (an API call) are reused before asking again.
RECENT_SECONDS = 5.0
TEMP_DIR = os.path.join(os.environ.get("TEMP", "."), "talon_jump_lists")

CLSID_ApplicationDocumentLists = "{86BEC222-30F2-47E0-9F25-60D11CD75C28}"
IID_IApplicationDocumentLists = "{3C594F9F-9F30-47A1-979A-C9E83D3D0A06}"
CLSID_ApplicationDestinations = "{86C14003-4D6B-4EF3-A7B4-0506663B2E68}"
IID_IApplicationDestinations = "{12337D35-94C6-48A0-BCE7-6A9C69D4D600}"
IID_IObjectArray = "{92CA9DCD-5622-4BBA-A805-5E9F541BD8C9}"
IID_IPersistStream = "{00000109-0000-0000-C000-000000000046}"
PKEY_Title = ("{F29F85E0-4FF9-1068-AB91-08002B27B3D9}", 2)
PKEY_IsDestListSeparator = ("{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}", 6)
PKEY_ActivationContext = ("{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}", 20)
PKEY_AppUserModel_PackageInstallPath = ("{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}", 15)
PKEY_AppUserModel_DestListLogoUri = ("{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}", 29)
CLSID_ApplicationActivationManager = "{45BA127D-10A8-46EA-8AB7-56EA9078943C}"
IID_IApplicationActivationManager = "{2E941141-7F97-4756-BA1D-9DECDE894A3D}"
CLSCTX_ALL = 0x17
CLSID_AutomaticDestinationList = "{F0AE1542-F497-484B-A175-A20DB09144BA}"
IID_IAutomaticDestinationList10b = "{E9C5EF8D-FD41-4F72-BA87-EB03BAD5817C}"
# Its vtable (checked on Windows 11 build 26300): Initialize 3, HasList 4, GetList 5,
# AddUsagePoint 6, PinItem 7, IsPinned 8, RemoveDestination 9.
ADL_INITIALIZE, ADL_GET_LIST, ADL_PIN_ITEM, ADL_REMOVE = 3, 5, 7, 9
DESTLIST_PINNED = 0
PIN_APPEND, UNPIN = -1, -2
PINNED_ITEMS = 20

if app.platform == "windows":
    ole32 = ctypes.WinDLL("ole32")
    shlwapi = ctypes.WinDLL("shlwapi")
    ole32.CoCreateInstance.argtypes = [PTR, PTR, wintypes.DWORD, PTR, PTR]
    ole32.CoCreateInstance.restype = HRESULT
    ole32.CoInitializeEx.argtypes = [PTR, wintypes.DWORD]
    ole32.CoInitializeEx.restype = HRESULT
    shlwapi.SHCreateMemStream.argtypes = [ctypes.c_char_p, wintypes.UINT]
    shlwapi.SHCreateMemStream.restype = PTR


@dataclass
class JumpEntry:
    title: str
    # "link": a serialized ShellLink (`data`); "item": a recent or frequent shell item
    # (`path`, its parsing name); "separator".
    kind: str
    data: bytes = b""
    path: str = ""


@dataclass
class JumpCategory:
    name: str
    entries: list = field(default_factory=list)
    # Recent and frequent items can be removed from the list.
    removable: bool = False
    # "pinned", "recent" (and frequent), "custom" (an app category: VS Code's "Recent
    # Folders", Edge's "Top Sites") or "tasks": what can be done with its entries.
    kind: str = "custom"


@dataclass
class JumpList:
    app_id: str
    categories: list


def app_id_hash(app_id: str) -> str:
    """The file name the shell uses for an app's jump lists."""
    crc = 0xFFFFFFFFFFFFFFFF
    for byte in app_id.upper().encode("utf-16-le"):
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0x92C64265D32139A4 if crc & 1 else crc >> 1
    return "%016x" % crc


def _create(clsid: str, iid: str) -> PTR | None:
    obj = PTR()
    if ole32.CoCreateInstance(ref(GUID(clsid)), None, shell_com.CLSCTX_INPROC_SERVER, ref(GUID(iid)), ref(obj)) != 0 or not obj:
        return None
    return obj


def _load_link(data: bytes) -> tuple[PTR | None, int]:
    """A ShellLink loaded from serialized bytes, and how many bytes it used."""
    stream = shlwapi.SHCreateMemStream(data, len(data))
    if not stream:
        return None, 0
    link = _create(shell_com.CLSID_ShellLink, shell_com.IID_IShellLinkW)
    used = 0
    try:
        if link is None:
            return None, 0
        persist = shell_com.query_interface(link, IID_IPersistStream)
        if persist is None:
            release(link)
            return None, 0
        try:
            if call(persist, 5, HRESULT, PTR(stream)) != 0:
                release(link)
                return None, 0
        finally:
            release(persist)
        position = ctypes.c_ulonglong()
        # IStream::Seek(0, STREAM_SEEK_CUR): how far Load read.
        call(PTR(stream), 5, HRESULT, ctypes.c_longlong(0), wintypes.DWORD(1), ref(position))
        used = position.value
        return link, used
    finally:
        release(PTR(stream))


def _link_title(link) -> tuple[str, bool]:
    """A link's display title (resolving "@file,-id" and ms-resource strings), and
    whether it's a separator."""
    title = separator = None
    store = shell_com.query_interface(link, shell_com.IID_IPropertyStore)
    if store is not None:
        try:
            title = shell_com.store_string(store, PKEY_Title)
            separator = shell_com.store_string(store, PKEY_IsDestListSeparator)
        finally:
            release(store)
    is_separator = bool(separator) and separator.strip().lower() not in ("0", "false")
    if title:
        resolved = shell_com.resolve_indirect(title)
        if resolved and not resolved.startswith("@"):
            return resolved, is_separator
    # No usable title: the target and its arguments.
    buf = ctypes.create_unicode_buffer(1024)
    call(link, 3, HRESULT, ctypes.cast(buf, ctypes.c_wchar_p), ctypes.c_int(1024), PTR(), wintypes.DWORD(0))
    target = os.path.basename(buf.value)
    call(link, 10, HRESULT, ctypes.cast(buf, ctypes.c_wchar_p), ctypes.c_int(1024))
    return (f"{target} {buf.value}".strip() or title or "?"), is_separator


def _parse_custom(path: str) -> list[tuple[str, int, list]]:
    """(category name, kind, entries) from a .customDestinations-ms file; known
    categories (recent, frequent) only mark where those lists go."""
    data = open(path, "rb").read()
    if len(data) < 12:
        return []
    _version, count, _reserved = struct.unpack_from("<III", data, 0)
    pos, categories = 12, []
    clsid_link = bytes(GUID(shell_com.CLSID_ShellLink))
    for _ in range(count):
        if pos + 4 > len(data):
            break
        (kind,) = struct.unpack_from("<I", data, pos)
        pos += 4
        name, entries = "", []
        if kind == CATEGORY_CUSTOM:
            (length,) = struct.unpack_from("<H", data, pos)
            name = data[pos + 2 : pos + 2 + 2 * length].decode("utf-16-le", "replace")
            pos += 2 + 2 * length
        elif kind == CATEGORY_KNOWN:
            (known,) = struct.unpack_from("<i", data, pos)
            pos += 4
            categories.append(("Frequent" if known == KDC_FREQUENT else "Recent", kind, []))
            if pos + 4 <= len(data) and struct.unpack_from("<I", data, pos)[0] == FOOTER:
                pos += 4
            continue
        elif kind == CATEGORY_TASKS:
            name = "Tasks"
        else:
            break
        (n,) = struct.unpack_from("<I", data, pos)
        pos += 4
        for _ in range(n):
            if data[pos : pos + 16] != clsid_link:
                return categories
            link, used = _load_link(data[pos + 16 :])
            if link is None or not used:
                return categories
            try:
                title, separator = _link_title(link)
            finally:
                release(link)
            serialized = data[pos + 16 : pos + 16 + used]
            entries.append(JumpEntry("", "separator") if separator else JumpEntry(title, "link", data=serialized))
            pos += 16 + used
        if pos + 4 <= len(data) and struct.unpack_from("<I", data, pos)[0] == FOOTER:
            pos += 4
        categories.append((name, kind, entries))
    return categories


def _document_items(app_id: str, list_type: int) -> list[JumpEntry]:
    """Recent or frequent items of an app (IApplicationDocumentLists)."""
    lists = _create(CLSID_ApplicationDocumentLists, IID_IApplicationDocumentLists)
    if lists is None:
        return []
    entries = []
    try:
        if call(lists, 3, HRESULT, ctypes.c_wchar_p(app_id)) != 0:
            return []
        array = PTR()
        if call(lists, 4, HRESULT, ctypes.c_int(list_type), wintypes.UINT(RECENT_ITEMS), ref(GUID(IID_IObjectArray)), ref(array)) != 0 or not array:
            return []
        try:
            count = wintypes.UINT()
            call(array, 3, HRESULT, ref(count))
            for i in range(count.value):
                item = PTR()
                if call(array, 4, HRESULT, wintypes.UINT(i), ref(GUID(shell_com.IID_IShellItem)), ref(item)) != 0 or not item:
                    continue
                try:
                    name = shell_com.item_name(item)
                    parsing = shell_com.item_name(item, shell_com.SIGDN_DESKTOPABSOLUTEPARSING)
                finally:
                    release(item)
                if name and parsing and all(e.path.lower() != parsing.lower() for e in entries):
                    entries.append(JumpEntry(name, "item", path=parsing))
        finally:
            release(array)
    finally:
        release(lists)
    return entries


def _destination_list(app_id: str) -> PTR | None:
    """The shell's IAutomaticDestinationList for an app, or None where it's missing."""
    obj = _create(CLSID_AutomaticDestinationList, IID_IAutomaticDestinationList10b)
    if obj is None:
        return None
    if call(obj, ADL_INITIALIZE, HRESULT, ctypes.c_wchar_p(app_id), ctypes.c_wchar_p(None), ctypes.c_wchar_p(None)) != 0:
        release(obj)
        return None
    return obj


def _serialize_link(link) -> bytes:
    """A ShellLink's bytes (IPersistStream::Save), to load it again later."""
    persist = shell_com.query_interface(link, IID_IPersistStream)
    if persist is None:
        return b""
    stream = shlwapi.SHCreateMemStream(None, 0)
    try:
        if call(persist, 6, HRESULT, PTR(stream), wintypes.BOOL(False)) != 0:
            return b""
        size = ctypes.c_ulonglong()
        call(PTR(stream), 5, HRESULT, ctypes.c_longlong(0), wintypes.DWORD(2), ref(size))
        call(PTR(stream), 5, HRESULT, ctypes.c_longlong(0), wintypes.DWORD(0), ref(ctypes.c_ulonglong()))
        buf = ctypes.create_string_buffer(size.value)
        read = wintypes.ULONG()
        call(PTR(stream), 3, HRESULT, ctypes.cast(buf, PTR), wintypes.ULONG(size.value), ref(read))
        return buf.raw[: read.value]
    finally:
        release(persist)
        release(PTR(stream))


def _pinned_items(app_id: str) -> list[JumpEntry]:
    """The app's pinned items, in order."""
    adl = _destination_list(app_id)
    if adl is None:
        return []
    entries = []
    try:
        array = PTR()
        if call(adl, ADL_GET_LIST, HRESULT, ctypes.c_int(DESTLIST_PINNED), ctypes.c_int(PINNED_ITEMS), ctypes.c_int(0), ref(GUID(IID_IObjectArray)), ref(array)) != 0 or not array:
            return []
        try:
            count = wintypes.UINT()
            call(array, 3, HRESULT, ref(count))
            for i in range(count.value):
                item = PTR()
                if call(array, 4, HRESULT, wintypes.UINT(i), ref(GUID(shell_com.IID_IShellItem)), ref(item)) == 0 and item:
                    try:
                        name = shell_com.item_name(item)
                        parsing = shell_com.item_name(item, shell_com.SIGDN_DESKTOPABSOLUTEPARSING)
                    finally:
                        release(item)
                    if name and parsing:
                        entries.append(JumpEntry(name, "item", path=parsing))
                    continue
                # A pinned link (an app's custom category item, e.g. a VS Code folder).
                link = PTR()
                if call(array, 4, HRESULT, wintypes.UINT(i), ref(GUID(shell_com.IID_IShellLinkW)), ref(link)) == 0 and link:
                    try:
                        title, _separator = _link_title(link)
                        data = _serialize_link(link)
                    finally:
                        release(link)
                    if data:
                        entries.append(JumpEntry(title, "link", data=data))
        finally:
            release(array)
    finally:
        release(adl)
    return entries


def _entry_object(entry: JumpEntry) -> PTR | None:
    """A COM object for an entry (a shell item or a ShellLink), released by the caller."""
    if entry.kind == "item":
        return shell_com.create_item(entry.path)
    if entry.kind == "link":
        return _load_link(entry.data)[0]
    return None


def _change(app_id: str, entry: JumpEntry, slot: int, *args) -> bool:
    adl = _destination_list(app_id)
    if adl is None:
        return False
    try:
        obj = _entry_object(entry)
        if obj is None:
            return False
        try:
            ok = call(adl, slot, HRESULT, obj, *args) == 0
        finally:
            release(obj)
    finally:
        release(adl)
    _forget(app_id)
    return ok


def _forget(app_id: str):
    for key in [k for k in _recent_cache if k[0] == app_id.lower()]:
        del _recent_cache[key]


@on_com_thread
def pin(app_id: str, entry: JumpEntry) -> bool:
    """Pin an entry to the app's jump list (at the end of Pinned), like the taskbar."""
    return _change(app_id, entry, ADL_PIN_ITEM, ctypes.c_int(PIN_APPEND))


@on_com_thread
def unpin(app_id: str, entry: JumpEntry) -> bool:
    """Unpin an entry from the app's jump list."""
    return _change(app_id, entry, ADL_PIN_ITEM, ctypes.c_int(UNPIN))


# app id (lowercase) -> (file mtime, parsed custom categories); and recent items.
_custom_cache: dict[str, tuple[float, list]] = {}
_recent_cache: dict[tuple[str, int], tuple[float, list]] = {}


def _files(app_id: str) -> tuple[str, str]:
    name = app_id_hash(app_id)
    return (
        os.path.join(CUSTOM_DIR, name + ".customDestinations-ms"),
        os.path.join(AUTOMATIC_DIR, name + ".automaticDestinations-ms"),
    )


def has_jump_list(app_id: str) -> bool:
    """Whether the shell keeps a jump list for this id (cheap: two file checks)."""
    return any(os.path.exists(path) for path in _files(app_id))


@on_com_thread
def jump_list(app_ids) -> JumpList | None:
    """The jump list of the first of `app_ids` that has one, or None."""
    for app_id in app_ids:
        if not app_id or not has_jump_list(app_id):
            continue
        custom_path, automatic_path = _files(app_id)
        key = app_id.lower()
        custom = []
        if os.path.exists(custom_path):
            mtime = os.path.getmtime(custom_path)
            cached = _custom_cache.get(key)
            if cached is None or cached[0] != mtime:
                try:
                    cached = (mtime, _parse_custom(custom_path))
                except (OSError, struct.error) as e:
                    print(f"jump_lists: {custom_path}: {e!r}")
                    cached = (mtime, [])
                _custom_cache[key] = cached
            custom = cached[1]

        def recent(list_type):
            now = time.monotonic()
            cached = _recent_cache.get((key, list_type))
            if cached is None or now - cached[0] > RECENT_SECONDS:
                cached = (now, _document_items(app_id, list_type) if os.path.exists(automatic_path) else [])
                _recent_cache[(key, list_type)] = cached
            return cached[1]

        def pinned():
            now = time.monotonic()
            cached = _recent_cache.get((key, "pinned"))
            if cached is None or now - cached[0] > RECENT_SECONDS:
                cached = (now, _pinned_items(app_id) if os.path.exists(automatic_path) else [])
                _recent_cache[(key, "pinned")] = cached
            return cached[1]

        pins = pinned()
        # Like the taskbar, pinned items don't show up again in other categories.
        pinned_paths = {e.path.lower() for e in pins if e.kind == "item"}
        pinned_titles = {e.title for e in pins}

        def unpinned(entries):
            return [
                e
                for e in entries
                if not (e.kind == "item" and e.path.lower() in pinned_paths) and e.title not in pinned_titles
            ]

        categories = [JumpCategory("Pinned", pins, kind="pinned")] if pins else []
        placed_recent = False
        for name, kind, entries in custom:
            if kind == CATEGORY_KNOWN:
                # The taskbar fills both known categories from the shell's recent list
                # (File Explorer's "Frequent" matches ADLT_RECENT, not ADLT_FREQUENT).
                items = unpinned(recent(ADLT_RECENT))
                if items:
                    categories.append(JumpCategory(name, items, removable=True, kind="recent"))
                placed_recent = True
            elif entries:
                kept = unpinned(entries)
                if any(e.kind != "separator" for e in kept):
                    categories.append(JumpCategory(name, kept, kind="tasks" if kind == CATEGORY_TASKS else "custom"))
        if not placed_recent:
            # Apps without a custom list (File Explorer): the shell shows recent items.
            items = unpinned(recent(ADLT_RECENT))
            if items:
                categories.insert(1 if pins else 0, JumpCategory("Recent", items, removable=True, kind="recent"))
        if categories:
            return JumpList(app_id, categories)
    return None


def _cleanup_temp():
    """Remove launch shortcuts left from earlier launches."""
    for path in glob.glob(os.path.join(TEMP_DIR, "*.lnk")):
        try:
            if time.time() - os.path.getmtime(path) > 60:
                os.remove(path)
        except OSError:
            pass


def _save_link(link) -> str:
    """Save a ShellLink as a temporary shortcut (removed a minute later); its path."""
    persist = shell_com.query_interface(link, shell_com.IID_IPersistFile)
    if persist is None:
        raise OSError("couldn't save the jump list entry")
    os.makedirs(TEMP_DIR, exist_ok=True)
    path = os.path.join(TEMP_DIR, f"{time.time_ns()}.lnk")
    try:
        # IPersistFile::Save(path, remember)
        if call(persist, 6, HRESULT, ctypes.c_wchar_p(path), wintypes.BOOL(True)) != 0:
            raise OSError("couldn't save the jump list entry")
    finally:
        release(persist)
    return path


def _logo_file(logo: str, app_id: str | None) -> str | None:
    """A jump list link's logo (System.AppUserModel.DestListLogoUri) as a file: a path,
    or an ms-appx:/// URI in the app's package, where the file may only exist with a
    scale or target size qualifier (Square44x44Logo.targetsize-32.png)."""
    if not logo.lower().startswith("ms-appx:///"):
        path = os.path.expandvars(logo)
        return path if os.path.isfile(path) else None
    if not app_id:
        return None
    item = shell_com.create_item(f"shell:AppsFolder\\{app_id}")
    if item is None:
        return None
    try:
        root = shell_com.item_property(item, PKEY_AppUserModel_PackageInstallPath)
    finally:
        release(item)
    if not root:
        return None
    path = os.path.normpath(os.path.join(root, logo[len("ms-appx:///") :].replace("/", os.sep)))
    if os.path.isfile(path):
        return path
    stem, ext = os.path.splitext(path)
    variants = sorted(glob.glob(glob.escape(stem) + ".*" + ext))

    def rank(variant: str) -> tuple:
        qualifiers = os.path.basename(variant)[len(os.path.basename(stem)) + 1 : -len(ext)].lower()
        # Plain before high contrast ones, and a light picture (contrast-black) before a
        # dark one on the dark menu (Calculator ships only those for some tasks); made
        # for 32 pixels or 200% (the menu shows them at 16 points); plain before theme
        # variants (altform-lightunplated).
        size = qualifiers.split("_")[0]
        return ("contrast-white" in qualifiers, "contrast-" in qualifiers, size not in ("targetsize-32", "scale-200"), "_" in qualifiers)

    return min(variants, key=rank) if variants else None


@on_com_thread
def icon_source(entry: JumpEntry, app_id: str | None = None) -> str | None:
    """A parsing name whose shell icon (or, for an image file, picture) is the entry's,
    as the taskbar shows it: a recent item's path; a link's logo (Windows Terminal's
    profile icons); a packaged app's task's app; or the link saved as a temporary
    shortcut (the shell resolves its icon location or target)."""
    _cleanup_temp()
    if entry.kind == "item":
        return entry.path or None
    if entry.kind != "link":
        return None
    link, _used = _load_link(entry.data)
    if link is None:
        return None
    try:
        store = shell_com.query_interface(link, shell_com.IID_IPropertyStore)
        if store is not None:
            try:
                logo = shell_com.store_string(store, PKEY_AppUserModel_DestListLogoUri)
            finally:
                release(store)
            if logo:
                # One that doesn't resolve (Ubuntu's points into another package)
                # shows no icon, as on the taskbar.
                return _logo_file(logo, app_id)
        packaged = _packaged_activation(link)
        if packaged is not None:
            # A packaged app's task (Calculator's "Scientific") shows the app's icon;
            # its shortcut would get a blank document's.
            return f"shell:AppsFolder\\{packaged[0]}"
        return _save_link(link)
    except OSError:
        return None
    finally:
        release(link)


@on_com_thread
def run(entry: JumpEntry, app_exe: str | None = None):
    """Open a jump list entry the way the shell does: a task or custom link through the
    shell (saved as a temporary shortcut, so exe tasks, URLs and packaged-app links
    work); a recent item with the app if it's an executable that takes a file,
    else with its default handler."""
    _cleanup_temp()
    if entry.kind == "link":
        link, _used = _load_link(entry.data)
        if link is None:
            raise OSError("couldn't load the jump list entry")
        packaged = _packaged_activation(link)
        if packaged is not None:
            # A packaged app's task (Calculator's "Scientific"): activate the app with
            # the task's activation context, as the shell does.
            release(link)
            _activate(*packaged)
            return
        try:
            path = _save_link(link)
        finally:
            release(link)
        os.startfile(path)
    elif entry.kind == "item":
        exe = (app_exe or "").lower()
        if app_exe and exe.endswith(".exe") and os.path.basename(exe) not in ("explorer.exe", "applicationframehost.exe"):
            import subprocess

            subprocess.Popen([app_exe, entry.path])
        else:
            os.startfile(entry.path)


def _packaged_activation(link) -> tuple[str, str] | None:
    """(AppUserModelID, arguments) of a packaged app's jump list link, else None."""
    store = shell_com.query_interface(link, shell_com.IID_IPropertyStore)
    if store is None:
        return None
    try:
        app_id = shell_com.store_string(store, shell_com.PKEY_AppUserModel_ID)
        context = shell_com.store_string(store, PKEY_ActivationContext) or ""
    finally:
        release(store)
    if not app_id or "!" not in app_id:
        return None
    buf = ctypes.create_unicode_buffer(1024)
    call(link, 3, HRESULT, ctypes.cast(buf, ctypes.c_wchar_p), ctypes.c_int(1024), PTR(), wintypes.DWORD(0))
    if buf.value and os.path.exists(buf.value):
        return None
    call(link, 10, HRESULT, ctypes.cast(buf, ctypes.c_wchar_p), ctypes.c_int(1024))
    return app_id, buf.value or context


def _activate(app_id: str, arguments: str):
    """Start a packaged app with arguments, on a short-lived thread of its own:
    ActivateApplication waits until the app is up, which would hold up the shared COM
    thread (and so the switchers) for seconds."""
    import threading

    def run():
        ole32.CoInitializeEx(None, 2)
        try:
            _activate_now(app_id, arguments)
        except OSError as e:
            print(f"jump_lists: starting {app_id}: {e}")
        finally:
            ole32.CoUninitialize()

    threading.Thread(target=run, name="jump list activation", daemon=True).start()


def _activate_now(app_id: str, arguments: str):
    """IApplicationActivationManager::ActivateApplication."""
    manager = PTR()
    if ole32.CoCreateInstance(ref(GUID(CLSID_ApplicationActivationManager)), None, CLSCTX_ALL, ref(GUID(IID_IApplicationActivationManager)), ref(manager)) != 0 or not manager:
        raise OSError("couldn't start the app")
    try:
        pid = wintypes.DWORD()
        hr = call(manager, 3, HRESULT, ctypes.c_wchar_p(app_id), ctypes.c_wchar_p(arguments), ctypes.c_int(0), ref(pid))
        if hr != 0:
            raise OSError(f"ActivateApplication failed: 0x{hr & 0xFFFFFFFF:08x}")
    finally:
        release(manager)


@on_com_thread
def remove(app_id: str, entry: JumpEntry) -> bool:
    """Remove an item from the app's jump list ("Remove from this list"), through the
    shell's destination list; IApplicationDestinations where that's missing."""
    if entry.kind not in ("item", "link"):
        return False
    if _destination_list_available():
        return _change(app_id, entry, ADL_REMOVE)
    destinations = _create(CLSID_ApplicationDestinations, IID_IApplicationDestinations)
    if destinations is None:
        return False
    try:
        if call(destinations, 3, HRESULT, ctypes.c_wchar_p(app_id)) != 0:
            return False
        obj = _entry_object(entry)
        if obj is None:
            return False
        try:
            ok = call(destinations, 4, HRESULT, obj) == 0
        finally:
            release(obj)
    finally:
        release(destinations)
    _forget(app_id)
    return ok


def _destination_list_available() -> bool:
    obj = _create(CLSID_AutomaticDestinationList, IID_IAutomaticDestinationList10b)
    if obj is None:
        return False
    release(obj)
    return True
