import os

from talon import Context, Module, actions, app

from ...core.gui.gui import open_gui

# we know to stop showing the new user message when the following path is defined
NEW_USER_MESSAGE_DISMISSAL_PATH = os.path.join(
    os.path.dirname(__file__), "new_user_message_dismissed"
)

if app.platform == "windows":
    talon_menu_location = "system tray"
elif app.platform == "mac":
    talon_menu_location = "status area"
else:
    talon_menu_location = "system tray or status area"


@open_gui(y=0)
def new_user_gui(ui, ui_wrapper):
    ui_wrapper.title("Welcome to Talon Community!")

    ui.label("For additional help or to close this:")
    ui.label(
        "You may click any of the following buttons or use the corresponding voice commands"
    )
    ui.label(
        "If a Community graphical user interface does not have an explanation of what to say for each button,"
    )
    ui.label(
        "    then each button will show the name of the equivalent voice command and"
    )
    ui.label(
        "    buttons corresponding to options in a list will have the command before the : and the option description after."
    )
    ui.label('You can reopen this message by saying: "New User Message"')

    ui_wrapper.spacing()

    ui.label("Open the Talon Wiki:")
    if ui_wrapper.command_button("open Talon Wiki"):
        actions.user.open_url("https://talon.wiki")
    ui.label(
        "Open a Slack channel where you can get help and talk with other Talon users:"
    )
    if ui_wrapper.command_button("open Talon Slack"):
        actions.user.open_url("http://talonvoice.slack.com/messages/help")
    ui.label("Open a webpage for helping new users learn how to use Talon:")
    if ui_wrapper.command_button("open Talon Practice"):
        actions.user.open_url("https://chaosparrot.github.io/talon_practice/")

    ui.separator()

    ui.label(
        f"You can see the Talon menu by clicking the Talon icon in the {talon_menu_location}"
    )

    ui.separator()

    ui.label("Close this message:")
    if ui_wrapper.command_button("message hide"):
        actions.user.new_user_message_hide()
    ui.label("Close this message and stop seeing it on startup:")
    if ui_wrapper.command_button("message dismiss"):
        actions.user.new_user_message_stop_showing_on_startup()
        actions.user.new_user_message_hide()


mod = Module()
mod.tag("new_user_message_showing", desc="The new user message gui is showing")

ctx = Context()


def show_new_user_message():
    """Show the new user message
    Having this show up on startup with a fresh install required calling a function instead of an action, which is why this function exists
    """
    new_user_gui.show()
    ctx.tags = ["user.new_user_message_showing"]


@mod.action_class
class Actions:
    def new_user_message_show():
        """Shows a useful gui intended for new users"""
        show_new_user_message()

    def new_user_message_hide():
        """Hides the new user message gui"""
        new_user_gui.hide()
        ctx.tags = []

    def new_user_message_stop_showing_on_startup():
        """Stops showing the new user message gui on startup"""
        with open(NEW_USER_MESSAGE_DISMISSAL_PATH, "w") as _:
            # this creates an empty file
            pass


def on_ready():
    if not os.path.exists(NEW_USER_MESSAGE_DISMISSAL_PATH):
        show_new_user_message()


app.register("ready", on_ready)
