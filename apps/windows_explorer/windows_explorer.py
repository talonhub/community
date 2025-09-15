"""
Windows Explorer Integration for Talon Voice Control

This module provides voice control integration for Windows File Explorer by:

1. LANGUAGE DETECTION & LOCALIZATION:
   - Detects system UI language (English, German, etc.)
   - Maps localized folder names to actual filesystem paths
   - Handles different Explorer window title formats per language (EN, DE)

2. WINDOW TITLE PROCESSING:
   - Strips Explorer-specific suffixes (e.g., "- File Explorer", multi-tab indicators)
   - Supports both single and multi-tab Explorer windows

3. FOLDER PATH RESOLUTION:
   - Maps standard folders (Desktop, Documents, Pictures, etc.) to actual paths
   - Handles OneDrive redirection automatically

4. PATH MAPPING & EXCLUSIONS:
   - Maps localized display names to actual filesystem paths
   - Excludes system dialogs and non-navigable windows
   - Handles user display name mapping for personalized folders

5. VOICE COMMAND ACTIONS:
   - Navigation (open parent, go to directory)
   - File operations (new folder, open file, properties)
   - Address bar control (focus, copy, navigate)
   - Terminal integration (open command prompt in current location)

TESTED WITH:
   - Windows 11 24H2, Version 10.0.26100 Build 26100
   - English and German system languages

KNOWN LIMITATIONS:
   - Nested localized standard folders (e.g., "Pictures/Screenshots")
   - WSL root folder navigation (e.g., "Linux/Ubuntu")
"""

import logging
import os
import re

from talon import Context, Module, actions, app, ui

# Windows-specific imports (conditional)
if app.platform == "windows":
    import ctypes
    import locale
    try:
        from win32com.shell import shell, shellcon
    except ImportError:
        shell = None
        shellcon = None
else:
    shell = None
    shellcon = None

# Configure logging
logger = logging.getLogger(__name__)
if logger.level == logging.NOTSET:
    logger.setLevel(logging.ERROR) # Set to DEBUG if you want to implement a new language mapping

# App definition
mod = Module()
apps = mod.apps

apps.windows_explorer = r"""
os: windows
and app.name: Windows Explorer
os: windows
and app.name: Windows-Explorer
os: windows
and app.exe: /^explorer\.exe$/i
"""

# many commands should work in most save/open dialog.
# note the "show options" stuff won't work
# unless the path is displayed in the title, which is rare for those
apps.windows_file_browser = """
os: windows
and app.name: /.*/
and title: /(Save|Open|Browse|Select)/
"""

ctx = Context()
ctx.matches = r"""
app: windows_explorer
app: windows_file_browser
"""

USER_PATH = os.path.expanduser("~")
STANDARD_FOLDERS = [
    "Desktop", "Documents", "Downloads", "Music", "OneDrive",
    "Pictures", "Videos", "Links", "Favorites", "Contacts"
]

KNOWN_FOLDER_GUIDS = {
    'Desktop': '{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}',
    'Documents': '{FDD39AD0-238F-46AF-ADB4-6C85480369C7}',
    'Downloads': '{374DE290-123F-4565-9164-39C4925E467B}',
    'Music': '{4BD8D571-6D19-48D3-BE97-422220080E43}',
    'Pictures': '{33E28130-4E1E-4676-835A-98395C3BC3BB}',
    'Videos': '{18989B1D-99B5-455B-841C-AB7C74E4DDFC}',
    'Links': '{bfb9d5e0-c6a9-404c-b2b2-ae6db6af4968}',
    'Favorites': '{1777F761-68AD-4D8A-87BD-30B759FA33DD}',
    'Contacts': '{56784854-C6CB-462b-8169-88E350ACB882}'
}

LANGUAGE_MAPPINGS = {
    "en": {
        "suffix_patterns": [
            r" and [0-9]+ more tabs - File Explorer$",
            r" and 1 more tab - File Explorer$",
            r" - File Explorer$",
        ],
        "excludes": ["", "This PC", "File Explorer", "Gallery", "Home", "Network"],
    },
    "de": {
        "suffix_patterns": [
            r" und [0-9]+ weitere Registerkarten – Explorer$",
            r" und 1 weitere Registerkarte – Explorer$",
            r" – Datei-Explorer$",
        ],
        "excludes": ["", "Dieser PC", "Datei-Explorer", "Katalog", "Start", "Netzwerk"],
    },
}

directories_to_remap = {}

# Utility functions
def _string_to_guid(guid_string):
    """Convert GUID string to ctypes GUID structure.
    
    Args:
        guid_string (str): GUID string in format '{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}'
        
    Returns:
        GUID: ctypes GUID structure
    """
    class GUID(ctypes.Structure):
        _fields_ = [
            ('Data1', ctypes.c_ulong),
            ('Data2', ctypes.c_ushort),
            ('Data3', ctypes.c_ushort),
            ('Data4', ctypes.c_ubyte * 8)
        ]
    
    guid_string = guid_string.strip('{}').replace('-', '')
    guid = GUID()
    guid.Data1 = int(guid_string[0:8], 16)
    guid.Data2 = int(guid_string[8:12], 16)
    guid.Data3 = int(guid_string[12:16], 16)
    for i in range(8):
        guid.Data4[i] = int(guid_string[16 + i*2:18 + i*2], 16)
    return guid

# Windows-specific functions
def get_system_language():
    """Detect system UI language and return language code.
    
    Returns:
        str: Two-letter language code (e.g., 'en', 'de') or 'en' as fallback.
    """
    try:
        ui_language_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        system_language = locale.windows_locale[ui_language_id]
        language_code = system_language.split("_")[0]
        logger.debug(f"windows_explorer.get_system_language: {system_language}, code: {language_code}")
        return language_code
    except KeyError:
        logger.error("windows_explorer.get_system_language: Language detection failed, defaulting to English")
        return "en"

def get_user_display_name():
    """Get Windows user display name for directory mapping.
    
    Returns:
        str or None: User's display name or None if retrieval fails.
    """
    try:
        GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
        NameDisplay = 3
        size = ctypes.pointer(ctypes.c_ulong(0))
        GetUserNameEx(NameDisplay, None, size)
        nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
        GetUserNameEx(NameDisplay, nameBuffer, size)
        return nameBuffer.value
    except Exception:
        return None

def get_localized_folder_name(folder_id):
    """Get localized display name for a known folder using Windows Shell API.
    
    Args:
        folder_id (str): Folder identifier (e.g., 'Documents', 'Desktop')
        
    Returns:
        str or None: Localized folder name or None if retrieval fails
    """
    if folder_id not in KNOWN_FOLDER_GUIDS:
        return None
        
    try:
        guid_str = KNOWN_FOLDER_GUIDS[folder_id]
        folder_guid = _string_to_guid(guid_str)
        IID_IShellItem = _string_to_guid('{43826d1e-e718-42ee-bc55-a1e261c37bfe}')
        
        shell32 = ctypes.windll.shell32
        ole32 = ctypes.windll.ole32
        ole32.CoInitialize(None)
        
        try:
            ppsi = ctypes.POINTER(ctypes.c_void_p)()
            hr = shell32.SHGetKnownFolderItem(
                ctypes.byref(folder_guid), 0, None,
                ctypes.byref(IID_IShellItem), ctypes.byref(ppsi)
            )
            
            if hr != 0 or not ppsi:
                return None
            
            display_name_ptr = ctypes.c_wchar_p()
            vtable = ctypes.cast(ppsi.contents, ctypes.POINTER(ctypes.c_void_p))
            get_display_name_func = ctypes.cast(
                vtable[5], 
                ctypes.WINFUNCTYPE(
                    ctypes.c_long, ctypes.c_void_p, ctypes.c_ulong,
                    ctypes.POINTER(ctypes.c_wchar_p)
                )
            )
            
            hr = get_display_name_func(ppsi, 0, ctypes.byref(display_name_ptr))
            
            if hr == 0 and display_name_ptr:
                display_name = display_name_ptr.value
                ole32.CoTaskMemFree(display_name_ptr)
                
                release_func = ctypes.cast(
                    vtable[2], 
                    ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)
                )
                release_func(ppsi)
                return display_name
            
            if ppsi:
                release_func = ctypes.cast(
                    vtable[2], 
                    ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)
                )
                release_func(ppsi)
                
        finally:
            ole32.CoUninitialize()
            
    except Exception as e:
        logger.exception(f"windows_explorer.get_localized_folder_name: Exception getting localized name for {folder_id}: {e}")
    
    return None

def get_folder_names():
    """Get localized folder names using Win32 Shell APIs with caching and fallback.
    
    Returns:
        dict: Mapping of folder keys to localized names (or English fallback)
    """
    global _localized_folder_cache
    if _localized_folder_cache:
        return _localized_folder_cache
        
    try:
        folder_names = {}
        for folder_key in STANDARD_FOLDERS:
            if folder_key == "OneDrive":
                folder_names[folder_key] = "OneDrive"
                continue
                
            try:
                localized_name = get_localized_folder_name(folder_key)
                folder_names[folder_key] = localized_name or folder_key
                # logger.debug(f"windows_explorer.get_folder_names: {folder_key} -> {folder_names[folder_key]}")
            except Exception as e:
                folder_names[folder_key] = folder_key
                logger.exception(f"windows_explorer.get_folder_names: API error for {folder_key}: {e}")
        
        _localized_folder_cache = folder_names
        return folder_names
    except Exception as e:
        logger.exception(f"windows_explorer.get_folder_names: API approach failed, using English fallback: {e}")
        return {folder: folder for folder in STANDARD_FOLDERS}

def get_folder_path(folder_key):
    """Get actual filesystem path for folder using Win32 API.
    
    Automatically handles OneDrive redirection and other folder redirections.
    
    Args:
        folder_key (str): Folder identifier (e.g., 'Documents', 'Desktop')
        
    Returns:
        str: Full filesystem path to the folder
    """
    if not shell:
        logger.error("windows_explorer.get_folder_path: pywin32 is not installed.")
        return os.path.join(USER_PATH, folder_key)
        
    if not hasattr(get_folder_path, '_folder_id_map'):
        get_folder_path._folder_id_map = {
            "Desktop": shellcon.FOLDERID_Desktop,
            "Documents": shellcon.FOLDERID_Documents,
            "Downloads": shellcon.FOLDERID_Downloads,
            "Music": shellcon.FOLDERID_Music,
            "OneDrive": shellcon.FOLDERID_OneDrive,
            "Pictures": shellcon.FOLDERID_Pictures,
            "Videos": shellcon.FOLDERID_Videos,
            "Links": shellcon.FOLDERID_Links,
            "Favorites": shellcon.FOLDERID_Favorites,
            "Contacts": shellcon.FOLDERID_Contacts,
        }
    
    folder_id = get_folder_path._folder_id_map.get(folder_key)
    if folder_id:
        try:
            return shell.SHGetKnownFolderPath(folder_id, 0)
        except Exception as e:
            logger.exception(f"windows_explorer.get_folder_path: SHGetKnownFolderPath failed for {folder_key}: {e}")
    
    return os.path.join(USER_PATH, folder_key)

# Directory mapping functions
def initialize_directory_mappings():
    """Ensure directory mappings are loaded (lazy initialization)."""
    global directories_to_remap
    if not directories_to_remap:
        try:
            folder_names = get_folder_names()
            mappings = {}
            
            for folder_key in STANDARD_FOLDERS:
                localized_name = folder_names.get(folder_key, folder_key)
                actual_path = get_folder_path(folder_key)
                mappings[localized_name] = actual_path
                logger.debug(f"windows_explorer.initialize_directory_mappings: {localized_name} -> {actual_path}")

            if user_display_name:
                mappings[user_display_name] = USER_PATH
                logger.debug(f"windows_explorer.initialize_directory_mappings: User mapping {user_display_name} -> {USER_PATH}")

            directories_to_remap = mappings
        except Exception as e:
            logger.exception(f"windows_explorer.initialize_directory_mappings: Failed to load directory mappings: {e}")
            directories_to_remap = {}


# Windows platform initialization
if app.platform == "windows":
    language_code = get_system_language()
    user_display_name = get_user_display_name()
    _localized_folder_cache = {}
    directories_to_remap = {}
    current_language_mapping = LANGUAGE_MAPPINGS.get(language_code, LANGUAGE_MAPPINGS["en"])
    logger.debug(f"windows_explorer: Windows platform init using language mapping for '{language_code}'")


# Path processing functions
def _strip_explorer_suffixes(path):
    """Remove Explorer-specific suffixes from window title.
    
    Args:
        path (str): Window title path
        
    Returns:
        str: Path with Explorer suffixes removed
    """
    if 'current_language_mapping' in globals():
        for pattern in current_language_mapping["suffix_patterns"]:
            match = re.search(pattern, path)
            if match:
                path = path[:match.start()]
                logger.debug(f"windows_explorer._strip_explorer_suffixes: Stripped suffix from '{path}'")
                break
    return path

def _apply_directory_mappings(path):
    """Apply localized to actual path mappings.
    
    Args:
        path (str): Localized path from window title
        
    Returns:
        str: Actual filesystem path or original path if no mapping exists
    """
    initialize_directory_mappings()
    if path in directories_to_remap:
        mapped_path = directories_to_remap[path]
        logger.debug(f"windows_explorer._apply_directory_mappings: {path} -> {mapped_path}")
        return mapped_path
    return path

def _handle_path_exclusions(path):
    """Handle excluded paths by hiding pickers and returning empty string.
    
    Args:
        path (str): Path to check for exclusion
        
    Returns:
        str: Empty string if excluded, original path otherwise
    """
    if 'current_language_mapping' in globals() and path in current_language_mapping["excludes"]:
        logger.debug(f"windows_explorer._handle_path_exclusions: Directory excluded '{path}'")
        actions.user.file_manager_hide_pickers()
        return ""
    return path


@ctx.action_class("user")
class UserActions:

    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_current_path():
        path = ui.active_window().title
        logger.debug(f"windows_explorer.UserActions.file_manager_current_path: Window title '{path}'")

        path = _strip_explorer_suffixes(path)
        path = _apply_directory_mappings(path)
        path = _handle_path_exclusions(path)
        logger.debug(f"windows_explorer.UserActions.file_manager_current_path: Final path '{path}'")
        return path

    def file_manager_terminal_here():
        actions.key("ctrl-l")
        actions.insert("cmd.exe")
        actions.key("enter")

    def file_manager_show_properties():
        actions.key("alt-enter")

    # Navigation actions
    def file_manager_open_directory(path: str):
        actions.key("ctrl-l")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        actions.user.file_manager_open_directory(volume)

    # File operations
    def file_manager_new_folder(name: str):
        actions.key("home")
        actions.key("ctrl-shift-n")
        actions.insert(name)

    def file_manager_open_file(path: str):
        actions.key("home")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_file(path: str):
        actions.key("home")
        actions.insert(path)

    # Address bar operations
    def address_focus():
        actions.key("ctrl-l")

    def address_copy_address():
        actions.key("ctrl-l")
        actions.edit.copy()

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
