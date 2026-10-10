from contextlib import suppress

from talon import Context, Module, actions, app


def compute_version_number() -> float:
    """Convert the Talon version string to a float by finding the longest prefix that is a valid float. This will only capture the first 2 dot separated numbers in the version"""
    version = app.version
    values = version.split(".")
    with suppress(ValueError):
        result = float(values[0])
        if len(values) > 1 and values[1].isdigit():
            result += float("0." + values[1])
        return result

    raise ValueError(
        f"Could not parse Talon version {version} while trying to decide if your versions of Community and Talon are compatible."
    )


incompatible_version_gui = None

mod = Module()
mod.tag(
    "incompatible_version_message_showing",
    desc="A message warning about a version incompatibility between Community and Talon is showing",
)

ctx = Context()


def on_ready():
    global incompatible_version_gui
    if compute_version_number() < 1:
        from talon import imgui

        # define this inside the if statement so that future Talon versions that remove imgui do not throw an exception
        @imgui.open()
        def gui(gui: imgui.GUI):
            gui.text(
                "You are using a version of the Community maintained voice command set"
            )
            gui.text("intended for Talon 1.0 on an older version of Talon.")
            gui.text(
                "You should either update Talon or download a compatible Community version."
            )
            gui.text(
                "The following button takes you to a page where you can download a"
            )
            gui.text("Community version compatible with Talon 0.4")
            if gui.button("open zero point four download page"):
                actions.user.open_zero_point_four_compatible_community_download_page()
                actions.user.hide_incompatible_version_message()
            if gui.button("version message hide"):
                actions.user.hide_incompatible_version_message()

        ctx.tags = ["user.incompatible_version_message_showing"]
        gui.show()
        incompatible_version_gui = gui


@mod.action_class
class Actions:
    def hide_incompatible_version_message():
        """Close the version incompatibility message"""
        if incompatible_version_gui:
            incompatible_version_gui.hide()
            ctx.tags = []

    def open_zero_point_four_compatible_community_download_page():
        """Open the page for downloading a Talon 0.4 compatible version of Community"""
        actions.user.open_url("https://github.com/talonhub/community/releases/tag/v0.4")


app.register("ready", on_ready)
