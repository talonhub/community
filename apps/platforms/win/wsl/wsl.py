from talon import Context, Module, actions, imgui, settings, ui, app
from talon.debug import log_exception
import os
import subprocess
import logging
import sys

mod = Module()
# Note: these context matches are specific to ubuntu, but there are other
# distros one can run under wsl, e.g. docker. for that matter, there are
# multiple ubuntu distros available. we need a more general way of detecting
# the current distro, and a way for the user to specify which distro to use
# for any particular operation. perhaps implement a generic_wsl module and
# then layer various distros on top of that?
mod.apps.ubuntu = """
os: windows
and app.name: ubuntu.exe
"""

ctx = Context()
ctx.matches = r"""
app: ubuntu
app: windows_terminal
and win.title: /Ubuntu/ 
"""
directories_to_remap = {}
directories_to_exclude = {}

user_path = os.path.expanduser("~")
if app.platform == "windows":
    is_windows = True
    import ctypes

    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)

    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    one_drive_path = os.path.expanduser(os.path.join("~", "OneDrive"))

    # this is probably not the correct way to check for onedrive, quick and dirty
    if os.path.isdir(os.path.expanduser(os.path.join("~", r"OneDrive\Desktop"))):
        default_folder = os.path.join("~", "Desktop")

        directories_to_remap = {
            "Desktop": os.path.join(one_drive_path, "Desktop"),
            "Documents": os.path.join(one_drive_path, "Documents"),
            "Downloads": os.path.join(user_path, "Downloads"),
            "Music": os.path.join(user_path, "Music"),
            "OneDrive": one_drive_path,
            "Pictures": os.path.join(one_drive_path, "Pictures"),
            "Videos": os.path.join(user_path, "Videos"),
        }
    else:
        # todo use expanduser for cross platform support
        directories_to_remap = {
            "Desktop": os.path.join(user_path, "Desktop"),
            "Documents": os.path.join(user_path, "Documents"),
            "Downloads": os.path.join(user_path, "Downloads"),
            "Music": os.path.join(user_path, "Music"),
            "OneDrive": one_drive_path,
            "Pictures": os.path.join(user_path, "Pictures"),
            "Videos": os.path.join(user_path, "Videos"),
        }

def get_win_path(wsl_path):
    # for testing
    #wsl_path = 'Ubuntu-20.04'
    #wsl_path = '/mnt/qube/woobee/woobee/woobit'
    #print(f"WINPATH: {wsl_path}")
    return run_wslpath(["-w"], wsl_path)

def get_usr_path():
    #print(f'USRPATH: {"~"}')
    return run_wslpath(["-a"], "~")

def get_wsl_path(win_path):
    #print(f"WSLPATH: {win_path}")
    return run_wslpath(["-u"], "'{}'".format(win_path))

# this command fails every once in a while, with no indication why.
# so, when that happens we just retry.
MAX_ATTEMPTS = 2
def run_wslpath(args, in_path):
    path = ""
    loop_num = 0

    while loop_num < MAX_ATTEMPTS:
        (path, error) = run_wsl(['wslpath', *args, in_path])
        if error:
            logging.error(f'run_wslpath(): failed to translate given path - attempt: {loop_num}, error: {error}')

            path = ""
        elif path:
            # got it, no need to loop and try again
            break

        loop_num += 1

    return path

# Note: seems WSL itself generates utf-16-le errors, whereas your guest os probably does not.
# - see https://github.com/microsoft/WSL/issues/4607 and related issures. Not sure how this
# behavior might differ when the system locale has been changed from the default.
#
# Anyways, these WSL errors require special handling so they are logged clearly. This is presumably
# worthwhile given the likely importance of any such messages. For example, which would you rather
# see in the log?
#
#   1. Nothing at all, even though there might be serious problems.
#
#   2. b'T\x00h\x00e\x00 \x00W\x00i\x00n\x00d\x00o\x00w\x00s\x00 \x00S\x00u\x00b\x00s\x00y\x00s\x00t\x00e\x00m\x00 \x00f\x00o\x00r\x00 \x00L\x00i\x00n\x00u\x00x\x00 \x00i\x00n\x00s\x00t\x00a\x00n\x00c\x00e\x00 \x00h\x00a\x00s\x00 \x00t\x00e\x00r\x00m\x00i\x00n\x00a\x00t\x00e\x00d\x00.\x00\r\x00\r\x00\n\x00'
#
#   3. The Windows Subsystem for Linux instance has terminated.
#
# The error above indicates the WSL distro is hung and this result detection mechanism is offline. When
# that happens, it takes a while for the command to return and the talon watchdog generates messages
# in the log that indicate a hang but we can provide more contextual detail. The prime thing to do here
# is to get word to the user that WSL is not responding normally. Note that, even after reaching this
# state, existing interactive wsl sessions continue to run and so the user may be unaware of the true
# source of their "talon problems". For more information, see https://github.com/microsoft/WSL/issues/5110
# and https://github.com/microsoft/WSL/issues/5318.
#
def _decode(value: bytes) -> str:
    # check to see if the given byte string looks like utf-16-le. results may not be correct for all
    # possible cases, but if there's a problem this code can be replaced with chardet (once that module
    # covers utf-16-le - see https://github.com/chardet/chardet/pull/109#discussion_r119149003). of
    # course, by that time wsl might not have the same problem anyways.
    if (len(value) % 2 == 0) and sum(value[1::2]) == 0:
        # looks like utf-16-le, see https://github.com/microsoft/WSL/issues/4607 (and related issues).
        decoded = value.decode('UTF-16-LE')
    else:
        decoded = value.decode()
    #print(f"_decode(): value is {value}")
    #print(f"_decode(): decoded is {decoded}.")
    return decoded.strip()

def _run_cmd(command_line):
    result = error = ""
    #print(f"_run_cmd(): RUNNING - command line is {command_line}.")
    try:
        # for testing
        #raise subprocess.CalledProcessError(-4294967295, command_line, 'The Windows Subsystem for Linux instance has terminated.'.encode('UTF-16-LE'))

        tmp = subprocess.check_output(command_line, stderr=subprocess.STDOUT)
        result = _decode(tmp)
        #print(f"RESULT: command: {' '.join(command_line)}, result: {result}")
    except subprocess.CalledProcessError as exc:
        result = ""

        # decode the error
        error = _decode(exc.output)

        # log additional info for this particular case
        if error == 'The Windows Subsystem for Linux instance has terminated.':
            logging.error(f'_run_cmd(): failed to run command - error: {error}')
            logging.error(f'_run_cmd(): - wsl path detection is offline')
            logging.error(f'_run_cmd(): - you need to restart your wsl session, e.g. "wsl --terminate <distro>; wsl"')
    except:
        result = ""
        log_exception(f'[_run_cmd()] {sys.exc_info()[1]}')

    # return results for the last attempt
    #print(f'_run_cmd(): RETURNING - result: {result}, error: {error}')
    return [result, error]

def run_wsl(args):
    # for testing
    if False:
        wsl_cmd_str = "nosuchcommand"
    else:
        wsl_cmd_str = "wsl"

    # now run the caller's command
    command_line = [ wsl_cmd_str ] + args
    result = _run_cmd(command_line)
    #print(f'run_wsl(): RETURNING - result: {result}')
    return result

@ctx.action_class('user')
class UserActions:
    def file_manager_refresh_title(): actions.skip()
    def file_manager_open_parent():
        actions.insert('cd ..')
        actions.key('enter')
    def file_manager_current_path():
        path = ui.active_window().title
        try:
            path = path.split(":")[1].lstrip()
        except:
            path = ""

        # print("current: " + path)
        if "~" in path:
            # the only way I could find to correctly support the user folder:
            # get absolute path of ~, and strip /mnt/x from the string
            abs_usr_path = get_usr_path()
            abs_usr_path = abs_usr_path[abs_usr_path.find("/home") : len(abs_usr_path)]
            path = path.replace("~", abs_usr_path)

        path = get_win_path(path)

        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            path = ""

        return path

    # def file_manager_terminal_here():
    #     actions.key("ctrl-l")
    #     actions.insert("cmd.exe")
    #     actions.key("enter")

    # def file_manager_show_properties():
    #     """Shows the properties for the file"""
    #     actions.key("alt-enter")
    def file_manager_open_user_directory(path: str):
        """expands and opens the user directory"""
        if path in directories_to_remap:
            path = directories_to_remap[path]

        path = os.path.expanduser(os.path.join("~", path))
        if ":" in path:
            path = get_wsl_path(path)

        actions.user.file_manager_open_directory(path)

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        if ":" in str(path):
            path = get_wsl_path(path)

        actions.insert('cd "{}"'.format(path))
        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert('"{}"'.format(path))

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.insert('mkdir "{}"'.format(name))

    def file_manager_open_file(path: str):
        actions.insert(path)
        # actions.key("enter")

    def file_manager_select_file(path: str):
        actions.insert(path)

    def file_manager_open_volume(volume: str):
        actions.user.file_manager_open_directory(volume)

    def terminal_list_directories():
        actions.insert("ls")
        actions.key("enter")

    def terminal_list_all_directories():
        actions.insert("ls -a")
        actions.key("enter")

    def terminal_change_directory(path: str):
        actions.insert("cd {}".format(path))
        if path:
            actions.key("enter")

    def terminal_change_directory_root():
        """Root of current drive"""
        actions.insert("cd /")
        actions.key("enter")

    def terminal_clear_screen():
        """Clear screen"""
        actions.key("ctrl-l")

    def terminal_run_last():
        actions.key("up enter")

    def terminal_kill_all():
        actions.key("ctrl-c")
        actions.insert("y")
        actions.key("enter")
