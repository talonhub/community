"""
Windows Explorer Integration for Talon Voice Control

This module provides voice control integration for Windows File Explorer by:

1. LANGUAGE DETECTION & LOCALIZATION:
   - Detects system UI language (English, German, etc.)
   - Maps localized folder names to actual filesystem paths
   - Handles different Explorer window title formats per language

2. WINDOW TITLE PROCESSING:
   - Strips Explorer-specific suffixes (e.g., "- File Explorer", multi-tab indicators)
   - Uses regex patterns to clean window titles for path extraction
   - Supports both single and multi-tab Explorer windows

3. ONEDRIVE INTEGRATION:
   - Detects OneDrive installation and folder structure
   - Maps standard folders (Desktop, Documents, Pictures) to OneDrive paths when applicable
   - Handles hybrid OneDrive/local folder scenarios

4. PATH MAPPING & EXCLUSIONS:
   - Maps localized display names to actual filesystem paths
   - Excludes system dialogs and non-navigable windows
   - Handles user display name mapping for personalized folders

5. VOICE COMMAND ACTIONS:
   - Navigation (open parent, go to directory)
   - File operations (new folder, open file, properties)
   - Address bar control (focus, copy, navigate)
   - Terminal integration (open command prompt in current location)

This has been tested with:
   - Windows 11 24H2, Version 10.0.26100 Build 26100, English and German system language
"""

import logging
import os
import re

from talon import Context, Module, actions, app, ui

# Configuration
DEBUG_LOGGING = False

# Configure logging
if DEBUG_LOGGING:
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

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

# Global variables
user_path = os.path.expanduser("~")
directories_to_remap = {}
directories_to_exclude = []
title_suffix_patterns = []


def get_system_language():
    """Detect system UI language and return language code."""
    try:
        ui_language_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        system_language = locale.windows_locale[ui_language_id]
        language_code = system_language.split("_")[0]
        if DEBUG_LOGGING:
            logging.debug(
                f"Detected system language: {system_language}, code: {language_code}"
            )
        return language_code
    except KeyError:
        if DEBUG_LOGGING:
            logging.debug("Language detection failed, defaulting to English")
        return "en"


def get_user_display_name():
    """Get Windows user display name for directory mapping."""
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


if app.platform == "windows":
    import ctypes
    import locale

    language_code = get_system_language()
    user_display_name = get_user_display_name()
    # Standard Windows folder names (always in English)
    STANDARD_FOLDERS = [
        "Desktop",
        "Documents",
        "Downloads",
        "Music",
        "OneDrive",
        "Pictures",
        "Videos",
        "Links",
        "Favorites",
        "Contacts",
    ]

    # Language-specific mappings with standardized structure
    # TODO: Contributors - Add your language mappings here!
    # Each language needs: suffix_patterns, folder_names, excludes
    # See existing 'en' and 'de' entries as templates
    # -> Set DEBUG_LOGGING = True
    language_mappings = {
        "en": {
            "suffix_patterns": [
                r" and [0-9]+ more tabs - File Explorer$",
                r" and 1 more tab - File Explorer$",
                r" - File Explorer$",
            ],
            "folder_names": {
                "Desktop": "Desktop",
                "Documents": "Documents",
                "Downloads": "Downloads",
                "Music": "Music",
                "OneDrive": "OneDrive",
                "Pictures": "Pictures",
                "Videos": "Videos",
                "Links": "Links",
                "Favorites": "Favorites",
                "Contacts": "Contacts",
            },
            "excludes": [
                "Task Switching",
                "Task View",
                "This PC",
                "File Explorer",
                "Program Manager",
                "Run",
                "Gallery",
                "Home",
            ],
        },
        "de": {
            "suffix_patterns": [
                r" und [0-9]+ weitere Registerkarten – Explorer$",
                r" und 1 weitere Registerkarte – Explorer$",
                r" – Datei-Explorer$",
            ],
            "folder_names": {  # Right side is the localized name
                "Desktop": "Desktop",
                "Documents": "Dokumente",
                "Downloads": "Downloads",
                "Music": "Musik",
                "OneDrive": "OneDrive",
                "Pictures": "Bilder",
                "Videos": "Videos",
                "Links": "Links",
                "Favorites": "Favoriten",
                "Contacts": "Kontakte",
            },
            "excludes": [
                "Dieser PC",
                "Datei-Explorer",
                "Ausführen",
                "Katalog",
                "Start",
            ],
        },
    }

    def merge_language_mappings(base_mapping, language_code, language_mappings):
        """Merge language-specific mappings with base English mapping."""
        if language_code == "en" or language_code not in language_mappings:
            return base_mapping

        lang_specific = language_mappings[language_code]
        if DEBUG_LOGGING:
            logging.debug(
                f"Loading patterns for '{language_code}': {lang_specific.get('suffix_patterns', [])}"
            )

        # Merge each component safely
        for key in ["suffix_patterns", "excludes"]:
            if key in lang_specific and isinstance(lang_specific[key], list):
                base_mapping[key].extend(lang_specific[key])

        if "folder_names" in lang_specific and isinstance(
            lang_specific["folder_names"], dict
        ):
            base_mapping["folder_names"].update(lang_specific["folder_names"])

        return base_mapping

    # Build current language mapping
    current_language_mapping = merge_language_mappings(
        language_mappings["en"].copy(), language_code, language_mappings
    )

    title_suffix_patterns = current_language_mapping["suffix_patterns"]

    def setup_onedrive_detection():
        """Detect OneDrive and return path resolver function."""
        one_drive_path = os.path.expanduser(os.path.join("~", "OneDrive"))
        has_onedrive_desktop = os.path.isdir(os.path.join(one_drive_path, "Desktop"))

        if DEBUG_LOGGING:
            logging.debug(
                f"OneDrive: path={one_drive_path}, has_desktop={has_onedrive_desktop}"
            )

        def get_folder_path(folder_key):
            """Get actual filesystem path for folder (OneDrive-aware)."""
            if has_onedrive_desktop and folder_key in [
                "Desktop",
                "Documents",
                "Pictures",
            ]:
                return os.path.join(one_drive_path, folder_key)
            elif folder_key == "OneDrive":
                return one_drive_path
            else:
                return os.path.join(user_path, folder_key)

        return get_folder_path

    get_folder_path = setup_onedrive_detection()

    def build_directory_mappings(folder_names, get_folder_path, user_display_name):
        """Build directory remapping dictionary."""
        mappings = {}

        # Map standard folders
        for folder_key in STANDARD_FOLDERS:
            localized_name = folder_names.get(folder_key, folder_key)
            actual_path = get_folder_path(folder_key)
            mappings[localized_name] = actual_path

            if DEBUG_LOGGING:
                logging.debug(f"Directory mapping: {localized_name} -> {actual_path}")

        # Add user display name mapping if available
        if user_display_name:
            mappings[user_display_name] = user_path
            if DEBUG_LOGGING:
                logging.debug(f"User mapping: {user_display_name} -> {user_path}")

        return mappings

    # Initialize directory mappings and exclusions
    directories_to_remap = build_directory_mappings(
        current_language_mapping["folder_names"], get_folder_path, user_display_name
    )

    directories_to_exclude = [""] + current_language_mapping["excludes"]
    if DEBUG_LOGGING:
        logging.debug(f"Directories to exclude: {directories_to_exclude}")


def _strip_explorer_suffixes(path):
    """Remove Explorer-specific suffixes from window title."""
    for pattern in title_suffix_patterns:
        if DEBUG_LOGGING:
            logging.debug(f"Testing pattern '{pattern}' against '{path}'")
        match = re.search(pattern, path)
        if match:
            path = path[: match.start()]
            if DEBUG_LOGGING:
                logging.debug(f"Stripped pattern '{pattern}': {path}")
            break
        elif DEBUG_LOGGING:
            logging.debug(f"Pattern '{pattern}' did not match")
    return path


def _apply_directory_mappings(path):
    """Apply localized to actual path mappings."""
    if path in directories_to_remap:
        mapped_path = directories_to_remap[path]
        if DEBUG_LOGGING:
            logging.debug(f"Directory remapped: {path} -> {mapped_path}")
        return mapped_path
    return path


def _handle_path_exclusions(path):
    """Handle excluded paths by hiding pickers and returning empty string."""
    if path in directories_to_exclude:
        if DEBUG_LOGGING:
            logging.debug(f"Directory excluded: {path}")
        actions.user.file_manager_hide_pickers()
        return ""
    return path


@ctx.action_class("user")
class UserActions:

    def file_manager_open_parent():
        """Navigate to parent directory."""
        actions.key("alt-up")

    def file_manager_current_path():
        """Extract and process current file manager path from window title."""
        path = ui.active_window().title
        if DEBUG_LOGGING:
            logging.debug(f"Original window title: {path}")

        # Process path through pipeline
        path = _strip_explorer_suffixes(path)
        path = _apply_directory_mappings(path)
        path = _handle_path_exclusions(path)

        if DEBUG_LOGGING:
            logging.debug(f"Final path: {path}")
        return path

    def file_manager_terminal_here():
        """Open command prompt in current directory."""
        actions.key("ctrl-l")
        actions.insert("cmd.exe")
        actions.key("enter")

    def file_manager_show_properties():
        """Show properties dialog for selected item."""
        actions.key("alt-enter")

    # Navigation actions
    def file_manager_open_directory(path: str):
        """Navigate to specified directory."""
        actions.key("ctrl-l")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """Select directory by typing its path."""
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        """Open specified volume/drive."""
        actions.user.file_manager_open_directory(volume)

    # File operations
    def file_manager_new_folder(name: str):
        """Create new folder with specified name."""
        actions.key("home")
        actions.key("ctrl-shift-n")
        actions.insert(name)

    def file_manager_open_file(path: str):
        """Open file at specified path."""
        actions.key("home")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_file(path: str):
        """Select file by typing its path."""
        actions.key("home")
        actions.insert(path)

    # Address bar operations
    def address_focus():
        """Focus the address bar."""
        actions.key("ctrl-l")

    def address_copy_address():
        """Copy current address to clipboard."""
        actions.key("ctrl-l")
        actions.edit.copy()

    def address_navigate(address: str):
        """Navigate to specified address."""
        actions.user.file_manager_open_directory(address)
