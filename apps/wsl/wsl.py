import logging
import os
import re
import subprocess
import sys

from talon import Context, Module, actions, app, ui
from talon.debug import log_exception

mod = Module()

ctx = Context()

# note: this context match is intentionally made more complex so that it is more specific
# than the context defined in apps/win/windows_terminal/windows_terminal.py (and thereby
# takes precedence).
ctx.matches = rf"""
app: windows_terminal
and tag: user.wsl
tag: user.wsl
"""

if app.platform == "windows":
    import atexit
    import platform

    import win32api
    import win32con
    import win32event

    wsl_distros = []

    key_event = None
    registry_key_handle = None

    # we expect the window title to begin with 'WSL:<distro> ' and end with ': <path>'.
    # this can be achieved by setting the window title in your .bashrc (or equivalent)
    # file and making use of the WSL_DISTRO_NAME environment variable.
    #
    # take, for example, the default .bashrc for Ubuntu-20.04 - the window title was set
    # by changing the prompt definition from this:
    #
    #     PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    #
    # to this:
    #
    #     PS1="\[\e]0;${debian_chroot:+($debian_chroot)}WSL:${WSL_DISTRO_NAME} \u@\h: \w\a\]$PS1"                                          ^^^^^^^^^^^^^^^^^^^^^^
    #
    # any other regex can be used below if your title is formatted differently. just be sure the
    # resulting capture groups contain the distro and the path, in that order.
    wsl_title_regex = re.compile(r"^WSL:([^\s]+)\s*.*@.*:\s*(.*)$")

    # prepare flags to use for registry calls
    registry_access_flags = win32con.KEY_READ
    # not sure if this check is important...I know the win32con.KEY_WOW64_64KEY value is needed
    # on my 64-bit windows install, but I don't know what happens on 32-bit installs...so,
    # playing it safe here.
    # https://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python/12578715
    if platform.machine().endswith("64"):
        registry_access_flags = registry_access_flags | win32con.KEY_WOW64_64KEY

    # close registry key, if open
    def _close_key():
        global registry_key_handle
        # print(f"_close_key(): {registry_key_handle}")
        if registry_key_handle:
            win32api.RegCloseKey(registry_key_handle)
            registry_key_handle = None

    # make sure registry is closed on exit
    def atexit():
        _close_key()

    # open the registry key containing the list of installed wsl distros
    def _initialize_key():
        global key_event, registry_key_handle, registry_access_flags

        try:
            # make sure the registry key is not currently open
            if registry_key_handle:
                _close_key()

            # get an event for monitoring registry updates
            key_event = win32event.CreateEvent(None, True, True, None)
            # print(f"KEY_EVENT: {key_event}")

            # open the registry key
            registry_key_handle = win32api.RegOpenKeyEx(
                win32con.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss",
                0,
                registry_access_flags,
            )
            # print(f"registry_key_handle: {registry_key_handle}")

            # register for registry change events
            win32api.RegNotifyChangeKeyValue(
                registry_key_handle,
                True,
                win32api.REG_NOTIFY_CHANGE_LAST_SET,
                key_event,
                True,
            )

            # trigger reading the list for the first time
            win32event.SetEvent(key_event)
        except OSError:
            log_exception(f"[_initialize_key()] {sys.exc_info()[1]}")

    # read the list of wsl distros from the registry
    def _update_wsl_distros():
        global ctx, registry_key_handle, wsl_distros, registry_access_flags

        # make sure registry is open
        if not registry_key_handle:
            _initialize_key()

        distro_handle = None
        try:
            # check for registry changes
            result = win32event.WaitForSingleObjectEx(key_event, 0, False)
            # for testing
            if False:
                print(f"WAIT - {result=} (looking for 'win32con.WAIT_OBJECT_0')")
                print(f"WAIT - {win32con.WAIT_OBJECT_0=})")
                print(f"WAIT - {win32con.WAIT_ABANDONED=})")
                print(f"WAIT - {win32con.WAIT_TIMEOUT=})")
            if result == win32con.WAIT_OBJECT_0:
                # registry has changed since we last read it, load the distros
                subkeys = win32api.RegEnumKeyEx(registry_key_handle)
                for subkey in subkeys:
                    # print(f'{subkey=}')

                    distro_handle = win32api.RegOpenKeyEx(
                        registry_key_handle, subkey[0], 0, registry_access_flags
                    )
                    # print(f"{distro_handle=}")

                    distro_name = win32api.RegQueryValueEx(
                        distro_handle, "DistributionName"
                    )[0]
                    # print(f'{distro_name=}')
                    wsl_distros.append(distro_name)

                    win32api.RegCloseKey(distro_handle)

                # reset the event, will be set by system if reg key changes
                win32event.ResetEvent(key_event)

            elif result != win32con.WAIT_TIMEOUT:
                # something unexpected happened
                error = win32api.GetLastError()
                _close_key()
                raise Exception(
                    "failed while checking for wsl registry updates: {result=}: {error=}"
                )
        except OSError:
            if distro_handle:
                win32api.RegCloseKey(distro_handle)
            log_exception(f"[_update_wsl_distros()] {sys.exc_info()[1]}")

        # print(f'{wsl_distros=}')

    def _parse_win_title():
        path = ui.active_window().title

        _update_wsl_distros()
        distro = None
        try:
            (distro, path) = re.match(wsl_title_regex, path).groups()
            if distro not in wsl_distros:
                raise Exception(f"Unknown wsl distro: {distro}")
                # log_exception(f'[_update_wsl_distros()] {sys.exc_info()[1]}')
        except:
            try:
                # select line tail following the last colon in the window title
                path = path.split(":")[-1].lstrip()
            except:
                path = ""

        # print(f'TITLE PARSE - distro is {distro}, path is {path}')
        return (distro, path)


directories_to_remap = {}
directories_to_exclude = {}

# some definitions used for error handling
termination_error = "The Windows Subsystem for Linux instance has terminated."
restart_message = 'wsl path detection is offline, you need to restart your wsl session, e.g. "wsl --terminate <distro>; wsl"'
path_detection_disable_title = "Talon - WSL path detection disabled"
path_detection_disable_notice = "WSL path detection has been disabled because new WSL sessions cannot be started. See the log for more detail."
path_detection_disabled = False

user_path = os.path.expanduser("~")
if app.platform == "windows":
    is_windows = True
    one_drive_path = os.path.expanduser(os.path.join("~", "OneDrive"))

    # this is probably not the correct way to check for onedrive, quick and dirty
    if os.path.isdir(os.path.expanduser(os.path.join("~", r"OneDrive\Desktop"))):
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


def get_win_path(wsl_path, distro=None):
    # for testing
    # wsl_path = 'Ubuntu-20.04'
    # wsl_path = '/mnt/qube/woobee/woobee/woobit'
    # print(f"WINPATH: {wsl_path}")
    return run_wslpath(["-w"], wsl_path, distro)


def get_usr_path(distro=None):
    # print(f'USRPATH: {"~"}')
    return run_wslpath(["-a"], "~", distro)


def get_wsl_path(win_path, distro=None):
    # print(f"WSLPATH: {win_path}")
    return run_wslpath(["-u"], f"'{win_path}'", distro)


def _disable_path_detection(notify=True):
    global path_detection_disabled
    path_detection_disabled = True
    if notify:
        app.notify(
            title=path_detection_disable_title, body=path_detection_disable_notice
        )


# this command fails every once in a while, with no indication why.
# so, when that happens we just retry.
MAX_ATTEMPTS = 2


def run_wslpath(args, in_path, in_distro=None):
    global path_detection_disabled
    path = ""

    if not path_detection_disabled:
        loop_num = 0

        while loop_num < MAX_ATTEMPTS:
            # print(f"_run_wslpath(): {path_detection_disabled=}.")
            (distro, path, error) = run_wsl(["wslpath", *args, in_path], in_distro)
            if error:
                if in_path == distro and error.endswith("No such file or directory"):
                    # for testing
                    # print(f"run_wslpath(): - ignoring expected failure.")

                    # this is expected. happens when running after the window is created
                    # but before the default title has been changed. no need to spam the
                    # console for this case, just let it pass.
                    pass
                else:
                    logging.error(
                        f"run_wslpath(): failed to translate given path - attempt: {loop_num}, error: {error}"
                    )

                path = ""
                if error == termination_error:
                    # disable this code until the user resets it
                    _disable_path_detection()
                    break
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
# Once the WSL distro is hung, every attempt to use it results in many repeated log messages like these:
#
# 2021-10-15 11:15:49 WARNING [watchdog] "talon.windows.ui._on_event" @30.0s (stalled)
# 2021-10-15 11:15:49 WARNING [watchdog] "user.knausj_talon.code.file_manager.win_event_handler"
#
# These messages are from code used to detect the current path from the window title, and it every time the
# focus shifts to a wsl context or the current path changes. This gets tiresome if you don't want to restart
# wsl immediately (because your existing sessions are still running and you want to finish working before
# restarting wsl).
#
# So, wsl path detection is disabled when this condition is first detected. The user
# must then re-enable the feature once the underlying problem has been resolved. This can be done by
# using the 'weasel reset path detection' voice command or simply reloading this file.


def _decode(value: bytes) -> str:
    # check to see if the given byte string looks like utf-16-le. results may not be correct for all
    # possible cases, but if there's a problem this code can be replaced with chardet (once that module
    # covers utf-16-le - see https://github.com/chardet/chardet/pull/109#discussion_r119149003). of
    # course, by that time wsl might not have the same problem anyways.
    if (len(value) % 2 == 0) and sum(value[1::2]) == 0:
        # looks like utf-16-le, see https://github.com/microsoft/WSL/issues/4607 (and related issues).
        decoded = value.decode("UTF-16-LE")
    else:
        decoded = value.decode()
    # print(f"_decode(): value is {value}")
    # print(f"_decode(): decoded is {decoded}.")
    return decoded.strip()


def _run_cmd(command_line):
    result = error = ""
    # print(f"_run_cmd(): RUNNING - command line is {command_line}.")
    try:
        # for testing
        # raise subprocess.CalledProcessError(-4294967295, command_line, termination_error.encode('UTF-16-LE'))

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        tmp = subprocess.check_output(
            command_line, stderr=subprocess.STDOUT, startupinfo=startupinfo
        )
        result = _decode(tmp)
        # print(f"RESULT: command: {' '.join(command_line)}, result: {result}")
    except subprocess.CalledProcessError as exc:
        result = ""

        # decode the error
        error = _decode(exc.output)

        # log additional info for this particular case
        if error == termination_error:
            logging.error(f"_run_cmd(): failed to run command - error: {error}")
            logging.error(f"_run_cmd(): - {restart_message}")
    except:
        result = ""
        log_exception(f"[_run_cmd()] {sys.exc_info()[1]}")

    # return results for the last attempt
    # print(f'_run_cmd(): RETURNING - result: {result}, error: {error}')
    return [result, error]


def run_wsl(args, distro=None):
    # for testing
    if False:
        wsl_cmd_str = "nosuchcommand"
    else:
        wsl_cmd_str = "wsl"

    # for testing
    # distro = "Debian"
    # distro = 'Ubuntu-20.04-ms-0'

    if not distro:
        # fetch the (default) distro first
        result = _run_cmd([wsl_cmd_str, "echo", "$WSL_DISTRO_NAME"])
        distro = result[0]
        if not distro:
            # if we can't fetch the distro, then the user's command is not likely to work
            # either. so, we just return any error information we have to the caller.
            # print(f'run_wsl(): RETURNING EARLY (no distro) - distro: {distro}, result: {result}')
            return [None] + result

    # now run the caller's command
    command_line = [wsl_cmd_str, "--distribution", distro] + args
    result = _run_cmd(command_line)
    # print(f'run_wsl(): RETURNING - distro: {distro}, result: {result}')
    return [distro] + result


def get_distro():
    return run_wsl(["\n"])[0]


@ctx.action_class("user")
class UserActions:
    def file_manager_refresh_title():
        actions.skip()

    def file_manager_open_parent():
        actions.insert("cd ..")
        actions.key("enter")

    def file_manager_current_path():
        global path_detection_disabled
        if path_detection_disabled:
            logging.warning(
                'Skipping WSL path detection - try "weasel reset path detection"'
            )
            return ""

        (distro, path) = _parse_win_title()

        if "~" in path:
            # the only way I could find to correctly support the user folder:
            # get absolute path of ~, and strip /mnt/x from the string
            abs_usr_path = get_usr_path(distro)
            abs_usr_path = abs_usr_path[abs_usr_path.find("/home") : len(abs_usr_path)]
            path = path.replace("~", abs_usr_path)

        path = get_win_path(path, distro)

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

    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        if ":" in str(path):
            path = get_wsl_path(path)

        actions.insert(f'cd "{path}"')
        actions.key("enter")
        actions.user.file_manager_refresh_title()

    def file_manager_select_directory(path: str):
        """selects the directory"""
        actions.insert(f'"{path}"')

    def file_manager_new_folder(name: str):
        """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
        actions.insert(f'mkdir "{name}"')

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
        actions.insert(f"cd {path}")
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


@mod.action_class
class Actions:
    def wsl_reset_path_detection():
        """reset wsl path detection"""
        global path_detection_disabled
        path_detection_disabled = False

    def wsl_speak():
        """ask each distro to say hello (in the log)"""
        results = []
        _update_wsl_distros()
        for in_distro in wsl_distros:
            (distro, result, error) = run_wsl(
                ["echo", 'Hello, my name is "${WSL_DISTRO_NAME}".'], in_distro
            )
            if error:
                logging.error(f"wsl_speak(): {error=}")
            else:
                # print(f'{result=}')
                if len(result) == 0:
                    result = f'Distro "{in_distro}" has nothing to say.'
                results.append(result)
        print("\n" + "\n".join(results))
