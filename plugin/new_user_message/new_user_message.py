import os

from talon import Context, Module, actions, app, imgui

# we know to stop showing the new user message when the following path is defined
NEW_USER_MESSAGE_DISMISSAL_PATH = os.path.join(
    os.path.dirname(__file__), "new_user_message_dismissed"
)


@imgui.open(y=0)
def new_user_gui(gui: imgui.GUI):
    gui.text("Welcome to the Talon Community Configuration!")
    gui.line()

    gui.text("For additional help or to close this:")
    gui.text(
        "You may click any of the following buttons or use the corresponding voice commands"
    )
    gui.text("Community buttons always show the name of the equivalent voice command")
    gui.text("Button text usually shows the exact voice command")
    gui.text(
        "Buttons corresponding to options in a list have the command before the : and the option description after"
    )
    gui.text('You can reopen this message by saying: "New User Message"')

    gui.spacer()

    gui.text("Open the Talon Wiki:")
    if gui.button("Open Talon Wiki"):
        actions.user.open_url("https://talon.wiki")
    gui.text(
        "Open a Slack channel where you can get help and talk with other Talon users:"
    )
    if gui.button("Open Talon Slack"):
        actions.user.open_url("http://talonvoice.slack.com/messages/help")
    gui.text("Open a webpage for helping new users learn how to use Talon:")
    if gui.button("Open Talon Practice"):
        actions.user.open_url("https://chaosparrot.github.io/talon_practice/")

    gui.line()

    gui.text(
        "You can see the Talon menu by right clicking the Talon icon in the system tray"
    )

    gui.line()

    gui.text("Close this message:")
    if gui.button("Message Hide"):
        actions.user.new_user_message_hide()
    gui.text("Close this message and stop seeing it on startup:")
    if gui.button("Message Dismiss"):
        actions.user.new_user_message_stop_showing_on_startup()
        actions.user.new_user_message_hide()


mod = Module()
mod.tag("new_user_message_showing", desc="The new user message gui is showing")

ctx = Context()


def show_new_user_message():
    """Show the new user message
    Having this show up on startup with a fresh and stall required calling a function instead of an action, which is why this function exists
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
