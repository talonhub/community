from typing import Tuple
from talon import Context, actions, app, ui
import os

ctx = Context()
ctx.matches = r"""
os: windows
"""

ctx.lists["self.system_setting"] = {
    "sound": "control mmsys.cpl sounds",
    "bluetooth": "control bthprops.cpl",
    "applications": "control appwiz.cpl",
    "display": "control desk.cpl",
    "taskbar": "control /name Microsoft.Taskbar",
    "programs and features": "control /name Microsoft.ProgramsAndFeatures",
    "Power": "control powercfg.cpl",
    "Mouse": "control main.cpl",
    "Keyboard": "control main.cpl keyboard",
    "Network": "control /name Microsoft.NetworkAndSharingCenter",
    "System Properties": "control sysdm.cpl",
    "User Accounts": "control userpasswords",
    "Internet Options": "control inetcpl.cpl",
    "Date and Time": "control timedate.cpl",
    "Device Manager": "control /name Microsoft.DeviceManager",
    "Ease of Access Center": "control /name Microsoft.EaseOfAccessCenter",
    "Administrative Tools": "control /name Microsoft.AdministrativeTools",
    "Default Programs": "control /name Microsoft.DefaultPrograms",
    "Windows Update": "control /name Microsoft.WindowsUpdate"
    # "Notifications": "control /name Microsoft.NotificationAreaIcons",
}

if app.platform == "windows":
    one_drive_path = os.path.expanduser(os.path.join("~", "OneDrive"))

    # this is probably not the correct way to check for onedrive, quick and dirty
    if os.path.isdir(os.path.expanduser(os.path.join("~", r"OneDrive\Desktop"))):
        default_folder = os.path.join("~", "Desktop")

        ctx.lists["self.system_directories"] = {
            "applications": "shell:AppsFolder",
            "desk": os.path.join(one_drive_path, "Desktop"),
            "docks": os.path.join(one_drive_path, "Documents"),
            "downloads": os.path.expanduser("~/Downloads"),
            "pictures": os.path.join(one_drive_path, "Pictures"),
            "one drive": one_drive_path,
            "user": os.path.expanduser("~"),
            "profile": os.path.expanduser("~"),
            "program files": os.path.expandvars("%ProgramFiles%"),
            "talent home": os.path.expandvars("%AppData%\\Talon"),
            "talent user": os.path.expandvars("%AppData%\\Talon\\user"),
            "talent recordings": os.path.expandvars("%AppData%\\talon\\recordings"),
            "talent recording": os.path.expandvars("%AppData%\\talon\\recordings"),
            "talent plugins": os.path.expandvars(
                "%ProgramFiles%\\Talon\\talon_plugins"
            ),
            "talent plugin": os.path.expandvars(
                "%ProgramFiles%\\Talon\\talon_plugins"
            ),
            "local app data": os.path.expandvars("%LocalAppData%"), 
            "app data": os.path.expandvars("%AppData%"),
            "rejects": os.path.expandvars("%AppData%\\talon\\recordings\\2024-11\\reject"), 
            "root": "\\",
        }

    else:
        ctx.lists["self.system_directories"] = {
            "applications": "shell:Applications",
            "desk": os.path.expanduser("~/Desktop"),
            "docks": os.path.expanduser("~/Documents"),
            "downloads": os.path.expanduser("~/Downloads"),
            "pictures": os.path.expanduser("~/Pictures"),
            "user": os.path.expanduser("~"),
            "profile": os.path.expanduser("~"),
            "program files": os.path.expandvars("%ProgramFiles%"),
            "talent home": os.path.expandvars("%AppData%\\Talon"),
            "talent user": os.path.expandvars("%AppData%\\Talon\\user"),
            "talent recordings": os.path.expandvars("%AppData%\\talon\\recordings"),
            "talent recording": os.path.expandvars("%AppData%\\talon\\recordings"),
            "talent plugins": os.path.expandvars(
                "%ProgramFiles%\\Talon\\talon_plugins"
            ),
            "talent plugin": os.path.expandvars(
                "%ProgramFiles%\\Talon\\talon_plugins"
            ),
            "local app data": os.path.expandvars("%LocalAppData%"), 
            "app data": os.path.expandvars("%AppData%"),
            "rejects": os.path.expandvars("%AppData%\\talon\\recordings\\2024-11\\reject"),
            "root": "\\",
        }

def get_selection(document_range, selection_range) -> Tuple[int, int]:
    """Get the selection from the Windows API"""
    range_before_selection = document_range.clone()
    range_before_selection.move_endpoint_by_range(
        "End",
        "Start",
        target=selection_range,
    )
    start = len(range_before_selection.text)

    range_after_selection = document_range.clone()
    range_after_selection.move_endpoint_by_range(
        "Start",
        "End",
        target=selection_range,
    )
    end = len(document_range.text) - len(range_after_selection.text)

    return start, end

@ctx.action_class("user")
class UserActionsWin:
    def dictation_peek(left, right):
        # Latency for this approach when I tested it with Slack in Firefox was <16ms.
        try:
            focused_element = ui.focused_element()
            # print("focused_element")
            text_pattern = focused_element.text_pattern
            # print("text_pattern")
            if not (text_pattern):
                # print("No text")
                return actions.next(left, right)
            
            document_range = text_pattern.document_range
            # print("document_range")
            document_text = document_range.text
            # print("document_text")
            selection_ranges = text_pattern.selection
            # print("Selection range")
            if len(selection_ranges) > 1:
                # Just act like there is no selection if there are multiple selections.
                print(
                    "WARNING: Multiple selections detected. This is not supported. Ignoring surrounding text."
                )
                return None
            # print("Selection found")
            selection_range = selection_ranges[0]
            selection_start, selection_end = get_selection(
                document_range, selection_range
            )

            chars_before_start = max(0, selection_start - 100)
            chars_after_end = min(len(document_text) - 1, selection_end + 100)
            return (
                document_text[chars_before_start:selection_start],
                document_text[selection_end:chars_after_end])
        except OSError as e:
            print(str(e))
            return actions.next(left, right)
        except Exception as e: 
            print(str(e))
            return actions.next(left, right)
                        
    
    def exec(command: str):
        actions.user.system_command_nb(command)

    def system_setting(system_setting: str):
        actions.user.exec(f'{system_setting}')

    def system_shutdown():
        shutdown("s")

    def system_restart():
        shutdown("r")

    def system_task_manager():
        actions.key("ctrl-shift-escape")
        
    def system_hibernate():
        shutdown("h")

    def system_lock():
        actions.user.sleep_all()
        actions.user.exec("rundll32.exe user32.dll,LockWorkStation")

    def system_show_desktop():
        actions.key("super-d")

    def system_task_view():
        actions.key("super-tab")

    def system_switcher():
        
        actions.key("ctrl-alt-tab")

    def system_search():
        actions.key("alt-space")

    def system_last_application():
        actions.key("alt-tab")

    def system_open_directory(path):
        path = os.path.expanduser(path)
        if os.path.exists(path):
            actions.user.exec(f'explorer.exe "{path}"')
        else:
            actions.app.notify(f"requested path {path} does not exist")

    def system_show_clipboard():
        actions.key("super-v")

    def system_kill_focused_application():
        """Kills the focused application"""
        for application in ui.apps(background=False):
            if application.name == actions.app.name():
                os.kill(application.pid, 0)

    def system_show_settings():
        actions.user.exec("start ms-settings:")
        # actions.user.switcher_launch("settings")

    def system_show_email(phrase: str = None):
        """Opens the defaul6t browser for the up operating system and performs the phrase command"""
        actions.key("super-2")
        actions.sleep("500ms")
        actions.user.parse_phrase(phrase or "")

    def system_show_messenger(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        # is_running = actions.user.switcher_focus(messaging_application.get())
        actions.key("super-3")
        actions.sleep("500ms")
        actions.user.parse_phrase(phrase or "")

    def system_show_slacker(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        actions.key("super-4")
        actions.sleep("500ms")
        actions.user.parse_phrase(phrase or "")

    def system_show_gitter(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        actions.key("super-5")
        actions.sleep("500ms")
        actions.user.parse_phrase(phrase or "")

    def system_show_portal(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        actions.key("super-6")
        actions.sleep("500ms")
        actions.user.parse_phrase(phrase or "")

    def system_show_coder(phrase: str = None):
        """Opens the default browser for the up operating system and performs the phrase command"""
        actions.key("super-7")
        actions.sleep("500ms")
        actions.user.parse_phrase(phrase or "")



def shutdown(flag: str):
    actions.key("super-r")
    actions.sleep("650ms")
    actions.insert(f"shutdown /{flag}")
