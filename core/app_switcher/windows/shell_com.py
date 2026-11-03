"""Minimal pure-ctypes COM and shell helpers, shared by the app switcher and the
thumbnail switcher.

COM objects are pointers to a vtable (an array of function pointers); `call` invokes
method number `slot` on one. Slots 0-2 are IUnknown's QueryInterface, AddRef and
Release.

Everything here must run on the shared COM thread (see com_thread.py): callers are
decorated with @on_com_thread, or only reached from such functions.
"""

import ctypes
from ctypes import wintypes

from talon import app

HRESULT = ctypes.c_long
PTR = ctypes.c_void_p

QUERY_INTERFACE = 0
RELEASE = 2

SIGDN_NORMALDISPLAY = 0x00000000
SIGDN_DESKTOPABSOLUTEPARSING = 0x80028000
CLSCTX_INPROC_SERVER = 0x1
STGM_READ = 0


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]

    def __init__(self, text: str | None = None):
        super().__init__()
        if text:
            ctypes.oledll.ole32.CLSIDFromString(text, ctypes.byref(self))

    @classmethod
    def parse(cls, text: str) -> "GUID":
        return cls(text)

    def key(self) -> bytes:
        return bytes(self)

    def __str__(self) -> str:
        d4 = bytes(self.Data4)
        return f"{self.Data1:08x}-{self.Data2:04x}-{self.Data3:04x}-{d4[:2].hex()}-{d4[2:].hex()}"


class PROPERTYKEY(ctypes.Structure):
    _fields_ = [("fmtid", GUID), ("pid", wintypes.DWORD)]

    def __init__(self, fmtid: str | None = None, pid: int = 0):
        super().__init__()
        if fmtid:
            self.fmtid = GUID(fmtid)
            self.pid = pid


class PROPVARIANT(ctypes.Structure):
    # Only read through PropVariantToStringAlloc, so the union stays opaque.
    _fields_ = [
        ("vt", ctypes.c_ushort),
        ("reserved1", ctypes.c_ushort),
        ("reserved2", ctypes.c_ushort),
        ("reserved3", ctypes.c_ushort),
        ("value", ctypes.c_void_p),
        ("extra", ctypes.c_void_p),
    ]


IID_IShellItem = "{43826D1E-E718-42EE-BC55-A1E261C37BFE}"
IID_IShellItem2 = "{7E9FB0D3-919F-4307-AB2E-9B1860310C93}"
IID_IEnumShellItems = "{70629033-E363-4A28-A567-0DB78006E6D7}"
IID_IPropertyStore = "{886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99}"
IID_IShellLinkW = "{000214F9-0000-0000-C000-000000000046}"
IID_IPersistFile = "{0000010B-0000-0000-C000-000000000046}"
CLSID_ShellLink = "{00021401-0000-0000-C000-000000000046}"
BHID_EnumItems = "{94F60519-2850-4924-AA5A-D15E84868039}"
BHID_PropertyStore = "{0384E1A4-1523-439C-A4C8-AB911052F586}"
# The virtual Applications folder: installed apps, Store apps included.
FOLDERID_AppsFolder = "{1E87508D-89C2-42F0-8A7E-645A0F50CA58}"
APPS_FOLDER_PREFIX = "::{4234D49B-0245-4DF3-B780-3893943456E1}\\"

PKEY_AppUserModel_ID = ("{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}", 5)
PKEY_AppUserModel_RelaunchDisplayNameResource = ("{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}", 4)
PKEY_Link_TargetParsingPath = ("{B9B4B3FC-2B51-4A42-B5D8-324146AFCF25}", 2)

if app.platform == "windows":
    ole32 = ctypes.WinDLL("ole32")
    shell32 = ctypes.WinDLL("shell32")
    propsys = ctypes.WinDLL("propsys")
    shlwapi = ctypes.WinDLL("shlwapi")
    ole32.CoTaskMemFree.argtypes = [PTR]
    ole32.CoTaskMemFree.restype = None
    ole32.PropVariantClear.argtypes = [PTR]
    ole32.CoCreateInstance.argtypes = [PTR, PTR, wintypes.DWORD, PTR, PTR]
    ole32.CoCreateInstance.restype = HRESULT
    shell32.SHCreateItemFromParsingName.argtypes = [wintypes.LPCWSTR, PTR, PTR, PTR]
    shell32.SHCreateItemFromParsingName.restype = HRESULT
    shell32.SHGetKnownFolderItem.argtypes = [PTR, wintypes.DWORD, wintypes.HANDLE, PTR, PTR]
    shell32.SHGetKnownFolderItem.restype = HRESULT
    shell32.SHGetKnownFolderPath.argtypes = [PTR, wintypes.DWORD, wintypes.HANDLE, PTR]
    shell32.SHGetKnownFolderPath.restype = HRESULT
    shell32.SHGetPropertyStoreForWindow.argtypes = [wintypes.HWND, PTR, PTR]
    shell32.SHGetPropertyStoreForWindow.restype = HRESULT
    propsys.PropVariantToStringAlloc.argtypes = [PTR, PTR]
    propsys.PropVariantToStringAlloc.restype = HRESULT
    shlwapi.SHLoadIndirectString.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.UINT, PTR]
    shlwapi.SHLoadIndirectString.restype = HRESULT


def ref(value) -> PTR:
    """A pointer to a ctypes value, typed as void* so it fits any declared argument."""
    return ctypes.cast(ctypes.pointer(value), PTR)


def call(obj, slot: int, restype, *args):
    """Call vtable method `slot` of the COM interface pointer `obj`; the argument types
    are taken from the ctypes values passed."""
    vtable = ctypes.cast(ctypes.cast(obj, ctypes.POINTER(PTR))[0], ctypes.POINTER(PTR))
    proto = ctypes.WINFUNCTYPE(restype, PTR, *[type(a) for a in args])
    return proto(vtable[slot])(obj, *args)


def release(obj):
    if obj:
        call(obj, RELEASE, wintypes.ULONG)


def query_interface(obj, iid: str) -> PTR | None:
    """Another interface of `obj` (released by the caller), or None."""
    out = PTR()
    if call(obj, QUERY_INTERFACE, HRESULT, ref(GUID(iid)), ref(out)) != 0 or not out:
        return None
    return out


def _take_string(pointer: ctypes.c_wchar_p) -> str | None:
    """A string the callee allocated with CoTaskMemAlloc, freed here."""
    try:
        return pointer.value or None
    finally:
        ole32.CoTaskMemFree(pointer)


def resolve_indirect(text: str | None) -> str | None:
    """Resolve "@file,-id" resource strings; other text is returned as it is."""
    if text and text.startswith("@"):
        resolved = ctypes.create_unicode_buffer(512)
        if shlwapi.SHLoadIndirectString(text, resolved, len(resolved), None) == 0:
            return resolved.value or None
    return text


def create_item(parsing_name: str, iid: str = IID_IShellItem) -> PTR | None:
    """A shell item for a path or shell: name (released by the caller), or None."""
    item = PTR()
    if shell32.SHCreateItemFromParsingName(parsing_name, None, ref(GUID(iid)), ref(item)) != 0 or not item:
        return None
    return item


def item_name(item, sigdn: int = SIGDN_NORMALDISPLAY) -> str | None:
    """IShellItem::GetDisplayName."""
    name = ctypes.c_wchar_p()
    if call(item, 5, HRESULT, ctypes.c_ulong(sigdn), ref(name)) != 0:
        return None
    return _take_string(name)


def store_string(store, key: tuple[str, int]) -> str | None:
    """A property from an IPropertyStore as a string, or None if absent or empty."""
    value = PROPVARIANT()
    if call(store, 5, HRESULT, ref(PROPERTYKEY(*key)), ref(value)) != 0:
        return None
    try:
        out = ctypes.c_wchar_p()
        if propsys.PropVariantToStringAlloc(ref(value), ref(out)) != 0:
            return None
        return _take_string(out)
    finally:
        ole32.PropVariantClear(ref(value))


def item_property(item, key: tuple[str, int]) -> str | None:
    """A shell item's property, through its property store (IShellItem::BindToHandler)."""
    store = PTR()
    if call(item, 3, HRESULT, PTR(), ref(GUID(BHID_PropertyStore)), ref(GUID(IID_IPropertyStore)), ref(store)) != 0 or not store:
        return None
    try:
        return store_string(store, key)
    finally:
        release(store)


def item_string(item, key: tuple[str, int]) -> str | None:
    """IShellItem2::GetString for a property, e.g. a shortcut's target."""
    item2 = query_interface(item, IID_IShellItem2)
    if item2 is None:
        return None
    try:
        value = ctypes.c_wchar_p()
        if call(item2, 17, HRESULT, ref(PROPERTYKEY(*key)), ref(value)) != 0:
            return None
        return _take_string(value)
    finally:
        release(item2)


def file_property(path: str, key: tuple[str, int]) -> str | None:
    """A property of a file, e.g. the AppUserModelID set on a shortcut."""
    item = create_item(path, IID_IShellItem2)
    if item is None:
        return None
    try:
        value = ctypes.c_wchar_p()
        if call(item, 17, HRESULT, ref(PROPERTYKEY(*key)), ref(value)) != 0:
            return None
        return _take_string(value)
    finally:
        release(item)


def window_property(hwnd: int, key: tuple[str, int]) -> str | None:
    """A property of a window's property store (AppUserModelID, relaunch name, ...)."""
    store = PTR()
    if shell32.SHGetPropertyStoreForWindow(hwnd, ref(GUID(IID_IPropertyStore)), ref(store)) != 0 or not store:
        return None
    try:
        return store_string(store, key)
    finally:
        release(store)


def known_folder_path(guid_text: str) -> str | None:
    path = ctypes.c_wchar_p()
    if shell32.SHGetKnownFolderPath(ref(GUID(guid_text)), 0, None, ref(path)) != 0:
        return None
    return _take_string(path)


def iter_folder_items(folder_id: str):
    """Yield each child IShellItem of a known folder. Each one is released once the
    loop moves on, so the loop body must not keep it."""
    folder = PTR()
    if shell32.SHGetKnownFolderItem(ref(GUID(folder_id)), 0, None, ref(GUID(IID_IShellItem)), ref(folder)) != 0 or not folder:
        return
    try:
        enum = PTR()
        if call(folder, 3, HRESULT, PTR(), ref(GUID(BHID_EnumItems)), ref(GUID(IID_IEnumShellItems)), ref(enum)) != 0 or not enum:
            return
        try:
            while True:
                child, fetched = PTR(), ctypes.c_ulong()
                # IEnumShellItems::Next; S_FALSE at the end.
                if call(enum, 3, HRESULT, ctypes.c_ulong(1), ref(child), ref(fetched)) < 0 or not fetched.value or not child:
                    break
                try:
                    yield child
                finally:
                    release(child)
        finally:
            release(enum)
    finally:
        release(folder)


def shortcut_target(lnk_path: str) -> tuple[str | None, str]:
    """A .lnk file's target path (None if it has none, e.g. a shell location) and its
    arguments ("" when there are none)."""
    link = PTR()
    if ole32.CoCreateInstance(ref(GUID(CLSID_ShellLink)), None, CLSCTX_INPROC_SERVER, ref(GUID(IID_IShellLinkW)), ref(link)) != 0 or not link:
        return None, ""
    target, arguments = None, ""
    try:
        persist = query_interface(link, IID_IPersistFile)
        if persist is None:
            return None, ""
        try:
            # IPersistFile::Load
            if call(persist, 5, HRESULT, ctypes.c_wchar_p(str(lnk_path)), wintypes.DWORD(STGM_READ)) != 0:
                return None, ""
        finally:
            release(persist)
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        # IShellLinkW::GetPath, without the find data.
        if call(link, 3, HRESULT, ctypes.cast(buf, ctypes.c_wchar_p), ctypes.c_int(wintypes.MAX_PATH), PTR(), wintypes.DWORD(0)) == 0:
            target = buf.value or None
        args = ctypes.create_unicode_buffer(1024)
        # IShellLinkW::GetArguments
        if call(link, 10, HRESULT, ctypes.cast(args, ctypes.c_wchar_p), ctypes.c_int(1024)) == 0:
            arguments = args.value
    finally:
        release(link)
    return target, arguments
