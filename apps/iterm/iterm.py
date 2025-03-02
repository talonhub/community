from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.iterm2 = """
os: mac
and app.bundle: com.googlecode.iterm2
"""
ctx.matches = r"""
app: iterm2
"""

directories_to_remap = {}
directories_to_exclude = {}


@ctx.action_class("edit")
class EditActions:
    def line_start():
        actions.key("home")

    def line_end():
        actions.key("end")


@ctx.action_class("user")
class UserActions:
    # def file_manager_current_path():
    #     title = ui.active_window().title

    #     if "~" in title:
    #         title = os.path.expanduser(title)

    #     if title in directories_to_remap:
    #         title = directories_to_remap[title]

    #     if title in directories_to_exclude:
    #         title = None

    #     return title

    # def file_manager_show_properties():
    #     """Shows the properties for the file"""

    # def file_manager_open_directory(path: str):
    #     """opens the directory that's already visible in the view"""
    #     actions.insert("cd ")
    #     path = '"{}"'.format(path)
    #     actions.insert(path)
    #     actions.key("enter")
    #     actions.user.file_manager_refresh_title()

    # def file_manager_select_directory(path: str):
    #     """selects the directory"""
    #     actions.insert(path)

    # def file_manager_new_folder(name: str):
    #     """Creates a new folder in a gui filemanager or inserts the command to do so for terminals"""
    #     name = '"{}"'.format(name)

    #     actions.insert("mkdir " + name)

    # def file_manager_open_file(path: str):
    #     """opens the file"""
    #     actions.insert(path)
    #     actions.key("enter")

    # def file_manager_select_file(path: str):
    #     """selects the file"""
    #     actions.insert(path)

    def tab_jump(number: int):
        actions.key(f"cmd-{number}")

    def tab_final():
        actions.key("cmd-9")

    def terminal_clear_screen():
        """Clear screen"""
        actions.key("ctrl-l")
