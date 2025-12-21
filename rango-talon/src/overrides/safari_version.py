import os
import subprocess
import plistlib

_SAFARI_BUNDLE = "com.apple.Safari"


def get_safari_version() -> str:
    try:
        return _get_app_version_by_bundle_id(_SAFARI_BUNDLE)
    except Exception as e:
        print("Exception retrieving safari version:", e.__class__, e)
        return "unknown"


def _get_app_version_by_bundle_id(id: str) -> str:
    """
    Returns the semantic version of the first application matching the supplied bundle id.

    See: https://developer.apple.com/documentation/bundleresources/information_property_list/cfbundleshortversionstring
    """
    for path in _find_app_paths_by_bundle_id(id):
        return _read_version_from_plist(path)
    return "unknown"


def _find_app_paths_by_bundle_id(id: str) -> list[str]:
    """Returns a list of paths to applications matching the supplied bundle id."""
    _subprocess_command = f'mdfind "kMDItemCFBundleIdentifier == {id}"'
    return subprocess.getoutput(_subprocess_command).splitlines()


def _read_version_from_plist(path: str) -> str:
    """Returns the semantic version string of the application at the supplied path."""
    with open(os.path.join(path, "Contents/Info.plist"), "rb") as f:
        return plistlib.load(f)["CFBundleShortVersionString"]
