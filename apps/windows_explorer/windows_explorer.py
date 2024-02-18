import os
import re

from talon import Context, Module, actions, app, ui, windows

mod = Module()
apps = mod.apps

apps.windows_explorer = """
os: windows
and app.name: Windows Explorer
os: windows
and app.name: Windows-Explorer
os: windows
and app.exe: /explorer.exe/i
"""

# many commands should work in most save/open dialog.
# note the "show options" stuff won't work unless work
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

# There are a few different ways the address bar needs to be found depending on the state of the window.
address_bar_criterion: list[list[dict[str]]] = [

        # File Explorer windows most of the time
        [
            {},  # Match any element for the root element
            {'automation_id': '40965'},  # 'class_name': 'ReBarWindow32'
            {'automation_id': '41477'},  # 'class_name': 'Address Band Root'
            {'class_name': 'msctls_progress32'},  # Progress bar
            {'class_name': 'Breadcrumb Parent'},  # Breadcrumb bar
            {'automation_id': '1001'}  # 'ToolbarWindow32'
        ],

        # File Explorer window when the address bar dropdown is open
        [
            {},  # Match any element for the root element
            {'automation_id': '40965'},  # ReBarWindow32
            {'automation_id': '41477'},  # Address Band Root
            {'class_name': 'msctls_progress32'},  # Progress bar
            {'name': 'Address band toolbar', 'class_name': 'ToolbarWindow32'},  # Address band toolbar
            {'control_type': 'Button', 'name': re.compile(r"Refresh .+ \(F5\)")}  # Refresh button
        ],
        # Title change events have the 'Address toolbar' as the root element
        [
            {'automation_id': '1001'}  # 'class_name': 'ToolbarWindow32'
        ],
    ]

user_path = os.path.expanduser("~")
directories_to_remap = {}
directories_to_exclude = {}

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

    if nameBuffer.value:
        directories_to_remap[nameBuffer.value] = user_path

    directories_to_exclude = [
        "",
        "Run",
        "Task Switching",
        "Task View",
        "This PC",
        "File Explorer",
        "Program Manager",
    ]


@ctx.action_class("user")
class UserActions:
    def file_manager_go_back():
        actions.key("alt-left")

    def file_manager_go_forward():
        actions.key("alt-right")

    def file_manager_open_parent():
        actions.key("alt-up")

    def file_manager_current_path():
        path = get_explorer_directory(ui.active_window())
        if path is None:
            # Fallback to the title of the window if the address could not be found
            path = ui.active_window().title

        if path in directories_to_remap:
            path = directories_to_remap[path]

        if path in directories_to_exclude:
            actions.user.file_manager_hide_pickers()
            path = ""

        return path

    def file_manager_terminal_here():
        actions.key("ctrl-l")
        actions.insert("cmd.exe")
        actions.key("enter")

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

    def file_manager_open_volume(volume: str):
        """file_manager_open_volume"""
        actions.user.file_manager_open_directory(volume)

def get_explorer_directory(window: ui.Window) -> str | None:
    """
    Returns the current directory in the given Windows Explorer window from the Address toolbar.
    """

    # Find the Address toolbar element
    current_element = None
    for element_navigator in address_bar_criterion:
        first_criteria = element_navigator[0]

        if not check_if_element_strictly_matches(window.element, **first_criteria):
            continue
        current_element = window.element
        for criterion in element_navigator[1:]:
            current_element = first_matching_child(current_element, **criterion)
            if current_element is None:
                break

        if current_element is not None:
            break

    if current_element is None:
        # The Address toolbar could not be found
        return None

    # Get the text from the Address toolbar or refresh button
    path = None
    if current_element.automation_id == "1001":
        path = current_element.name.replace("Address: ", "")
    elif current_element.control_type == "Button":
        path = current_element.name.replace('Refresh "', "").replace('" (F5)', "")

    return path


def check_if_element_strictly_matches(element: windows.ax.Element, **kw) -> bool:
    """
    Returns True if the given element matches all the given attribute-value pairs.
    The value of a pair may be a string or a regex pattern.

    Example:
        ```
        channel_element_name: re.Pattern = re.compile(r"(.+?).\\(channel\\)")
        element_matches: bool = check_if_element_strictly_matches(element, name=channel_element_name, control_type="Group")
        ```
        This will return True if the given `element` has an attribute `name`
          that matches the given regex pattern and `control_type` with the value "Group".

        ```
        element_matches: bool = check_if_element_strictly_matches(element, name="Channels", control_type="Group")
        ```
        This will return True if the given `element` has an attribute `name`
          with the value "Channels" and `control_type` with the value "Group".
    """

    # Iterate through the children of the element, checking if each one matches all the given attribute-value pairs
    for attr_name, match_value in kw.items():
        element_attr_value = getattr(element, attr_name)
        if isinstance(match_value, re.Pattern):
            if not match_value.search(element_attr_value):
                return False
        elif match_value != element_attr_value:
            return False
    return True

def first_matching_child(element: windows.ax.Element, **kw) -> windows.ax.Element | None:
    """
    Returns the first child element of `element` that matches all the given attribute-value pairs.
    The value may be a string or a regex pattern.

    Example:
        ```python
        child = first_matching_child(element, name="Channels", control_type="Group")
        ```
        This will return the first child of `element` that has an attribute `name` 
           with the value "Channels" and `control_type` with the value "Group".
    """

    return next(
        (
            e for e in element.children if check_if_element_strictly_matches(e, **kw)
        ), None
    )
