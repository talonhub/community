from talon import Context, Module, actions, clip, ui

mod = Module()
apps = mod.apps

# attempt to detect the standard file -> open file/folder dialog
apps.windows_open_dialog = r"""
os: windows
and app.name: /.*/
and win.class: #32770
and title: /(Save|Open|Browse|Select|Export)/
"""

ctx = Context()
ctx.matches = r"""
app: windows_open_dialog
"""


def get_path():
    path = None
    try:
        toolbar = ui.active_window().element.find_one(automation_id="1001", max_depth=0)
        if toolbar:
            path = toolbar.legacyiaccessible_pattern.name.replace("Address: ", "")
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
        return get_path()

    def file_manager_show_properties():
        actions.key("alt-enter")

    def file_manager_open_directory(path: str):
        actions.key("ctrl-l")
        actions.insert(path)
        actions.key("enter")

    def file_manager_select_directory(path: str):
        actions.insert(path)

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

    def file_manager_open_volume(volume: str):
        actions.user.file_manager_open_directory(volume)

    def address_focus():
        actions.key("ctrl-l")

    def address_copy_address():
        path = get_path()
        if path:
            clip.set_text(path)

    def address_navigate(address: str):
        actions.user.file_manager_open_directory(address)
