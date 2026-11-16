
from talon import Context, Module, actions, app, cron, ui, clip
import os

mod = Module()
apps = mod.apps

# the standard file -> open file/older dialog
# uses a fixed class name and supports most of the same
# actions defined for file explorer.
# Every standard dialog (message boxes, Run, Control Panel applets) is #32770, so
# user.file_dialog (below) narrows it to the ones hosting a shell folder view.
apps.windows_open_dialog = r"""
os: windows
and app.name: /.*/
and win.class: #32770
"""

ctx = Context()
ctx.matches = r"""
app: windows_open_dialog
user.file_dialog: true
"""

# --- user.file_dialog scope -------------------------------------------------
# "true" when the active window is a file dialog: a #32770 dialog containing a
# shell folder view (SHELLDLL_DefView). This depends only on window classes, so it
# works whatever the dialog's title or the Windows display language.

_file_dialog = {"file_dialog": "false"}
# Open dialogs create their folder view after they get focus (measured: up to
# about 0.4s, after the folder starts listing), so a dialog is looked at again
# until the view turns up or these run out.
RECHECK_DELAYS = ("150ms", "300ms", "500ms", "750ms", "1s", "1500ms", "2s", "3s")
_recheck_jobs = []


@mod.scope
def file_dialog_scope():
    return dict(_file_dialog)


if app.platform == "windows":
    import ctypes
    from ctypes import wintypes

    _user32 = ctypes.WinDLL("user32")
    _EnumChildProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    _user32.EnumChildWindows.argtypes = [wintypes.HWND, _EnumChildProc, wintypes.LPARAM]
    _user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]

    def _has_shell_view(hwnd: int) -> bool:
        found = False

        def visit(child, _):
            nonlocal found
            buf = ctypes.create_unicode_buffer(64)
            _user32.GetClassNameW(child, buf, len(buf))
            found = buf.value == "SHELLDLL_DefView"
            return not found  # stop enumerating once found

        _user32.EnumChildWindows(hwnd, _EnumChildProc(visit), 0)
        return found

    def _refresh(window):
        if window != ui.active_window():
            return
        is_dialog = getattr(window, "cls", None) == "#32770" and _has_shell_view(window.id)
        value = "true" if is_dialog else "false"
        if value != _file_dialog["file_dialog"]:
            _file_dialog["file_dialog"] = value
            file_dialog_scope.update()

    def _recheck(window):
        # Nothing left to find once the view is there.
        if _file_dialog["file_dialog"] != "true":
            _refresh(window)

    def _on_focus(window):
        for job in _recheck_jobs:
            cron.cancel(job)
        _recheck_jobs.clear()
        _refresh(window)
        # Only dialogs can turn into file dialogs.
        if getattr(window, "cls", None) == "#32770" and _file_dialog["file_dialog"] != "true":
            for delay in RECHECK_DELAYS:
                _recheck_jobs.append(cron.after(delay, lambda: _recheck(window)))

    def _register():
        ui.register("win_focus", _on_focus)
        _refresh(ui.active_window())

    app.register("ready", _register)

def get_path():
    """The text of the dialog's address bar: a path for ordinary folders, but a display
    name for some known folders and libraries (e.g. "Documents")."""
    path = None
    try:
        # Save dialogs also give the "File name:" box id 1001, so match the class too.
        toolbar = ui.active_window().element.find_one(
            automation_id="1001", class_name="ToolbarWindow32", max_depth=0
        )
        if toolbar:
            # "Address: C:\Windows"; the label is translated, so cut at the first ": ".
            name = toolbar.legacyiaccessible_pattern.name
            path = name.split(": ", 1)[1] if ": " in name else name
        else:
            print("Failed to retrieve toolbar for open dialog in active window")
    except:
        pass

    return path

@ctx.action_class("user")
class UserActions:
    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_current_path():
        path = get_path()
        # Only real folders; a display name like "Documents" would be read as a
        # path relative to Talon's working directory.
        if path and os.path.isabs(path) and os.path.isdir(path):
            return path
        return None

    def file_manager_show_properties():
        """Shows the properties for the file"""
        actions.key("alt-enter")

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        actions.key("ctrl-l")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(path)

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.key("home")
        actions.key("ctrl-shift-n")
        actions.insert(name)

    def file_manager_open_file(path: str):
        """opens the file"""
        actions.key("home")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_file(path: str):
        """selects the file"""
        actions.key("home")
        actions.insert(path)


    def file_manager_select_file(path: str):
        """selects the file"""
        actions.key("home")
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.user.file_manager_open_directory(volume)

    def address_focus():
        actions.key("ctrl-l")

    def address_copy_address():
        path = get_path()
        if path:
            clip.set_text(path)

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
