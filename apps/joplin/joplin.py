from talon import Context, Module, actions, app, settings

from ...core.command_client.command_client import run_command
from ...core.command_client.rpc_client.types import NoFileServerException
from ...core.notifications import debounce_notify

is_mac = app.platform == "mac"

mod = Module()


mod.apps.joplin = """
os: linux
and app.name: appimagekit-joplin
"""
mod.apps.joplin = """
os: mac
and app.bundle: net.cozic.joplin-desktop
"""
mod.apps.joplin = r"""
os: windows
and app.exe: /^joplin\.exe$/i
os: windows
app.name: Joplin
"""


lang_ctx = Context()
lang_ctx.matches = r"""
app: joplin
not tag: user.code_language_forced
"""

mod.setting(
    "joplin_use_command_server",
    type=bool,
    default=True,
    desc="""Whether to use the Joplin Command Server plugin (file-based RPC) instead of the Command Palette.
    When enabled, commands are sent via RPC and fall back to the Command Palette if the server directory is missing.
    However, the fallback can be slow, so it might be preferable to always bypass in some circumstances, e.g. with sandboxed Joplin.
    Set to False to bypass the command server and always use the Command Palette.""",
)


@lang_ctx.action_class("code")
class CodeActions:
    def language():
        return "markdown"

    def toggle_comment():
        actions.user.joplin("editor.toggleComment")


ctx = Context()
ctx.matches = r"""
app: joplin
"""

mac_ctx = Context()
mac_ctx.matches = r"""
os: mac
app: joplin
"""


ctx.tags = ["user.command_client"]


def joplin_palette_command(command_id: str):
    """Fallback execution via the Command Palette modal."""
    actions.user.command_search(command_id)
    actions.sleep("30ms")
    actions.key("enter")


def command_server_or_client_fallback(command_id: str, args: list | None = None):
    """Execute command via file RPC; automatically falls back to palette if server is absent."""
    if settings.get("user.joplin_use_command_server"):
        try:
            run_command(command_id, *(args or ()))
            return
        except NoFileServerException:
            debounce_notify(
                "joplin_command_server",
                "Command server failed; falling back to command palette. For better performance, install the Command Server plugin in Joplin: https://joplinapp.org/plugins/plugin/bluedrink9.CommandServer",
            )
        except Exception as e:
            debounce_notify(
                "joplin_command_server",
                "Command server failed; falling back to command palette.",
            )
            print(f"Joplin command server error: {e}")

    joplin_palette_command(command_id)


@mod.action_class
class Actions:
    def joplin(command_id: str, args: list = None):
        """Invoke an action by Joplin command id"""
        command_server_or_client_fallback(command_id, args)


@ctx.action_class("app")
class AppActions:
    def preferences():
        """Show Joplin settings window"""
        if is_mac:
            actions.key("cmd-,")
        else:
            actions.key("ctrl-,")

    def tab_open():
        actions.user.joplin("tabsPinNote")

    def tab_close():
        # Unpins/closes the active tab in Note Tabs
        actions.user.joplin("tabsUnpinNote")

    def tab_next():
        actions.user.joplin("tabsSwitchRight")

    def tab_previous():
        actions.user.joplin("tabsSwitchLeft")

    def tab_reopen():
        actions.user.joplin("tabsSwitchLastActive")

    def window_open():
        actions.user.joplin("openNoteInNewWindow")

    def window_close():
        if is_mac:
            actions.key("cmd-q")
        else:
            actions.key("ctrl-q")


@ctx.action_class("win")
class WinActions:
    def filename():
        title = actions.win.title()
        for suffix in (" - Joplin", " — Joplin"):
            if suffix in title:
                return title.split(suffix)[0]
        return title


@ctx.action_class("edit")
class EditActions:
    def undo():
        actions.user.joplin("editor.undo")

    def redo():
        actions.user.joplin("editor.redo")

    def copy():
        actions.user.joplin("textCopy")

    def cut():
        actions.user.joplin("textCut")

    def paste():
        actions.user.joplin("textPaste")

    def select_all():
        actions.user.joplin("textSelectAll")

    def save():
        actions.user.joplin("synchronize")

    def find(text: str | None = None):
        actions.user.joplin("showLocalSearch")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def find_next():
        actions.key("enter")

    def find_previous():
        actions.key("shift-enter")

    def line_swap_up():
        actions.user.joplin("editor.swapLineUp")

    def line_swap_down():
        actions.user.joplin("editor.swapLineDown")

    def line_clone():
        actions.user.joplin("editor.duplicateLine")

    def indent_more():
        actions.user.joplin("editor.indentMore")

    def indent_less():
        actions.user.joplin("editor.indentLess")

    def zoom_reset():
        if is_mac:
            actions.key("cmd-0")
        else:
            actions.key("ctrl-0")

    def zoom_in():
        if is_mac:
            actions.key("cmd-=")
        else:
            actions.key("ctrl-=")

    def zoom_out():
        if is_mac:
            actions.key("cmd--")
        else:
            actions.key("ctrl--")


@ctx.action_class("user")
class UserActions:
    def command_search(command: str = ""):
        """Show Joplin Command Palette"""
        if is_mac:
            actions.key("cmd-shift-p")
        else:
            actions.key("ctrl-shift-p")
        if command != "":
            actions.sleep("50ms")
            actions.insert(command)

    def command_server_directory() -> str:
        return "joplin-command-server"

    def go_back():
        actions.user.joplin("historyBackward")

    def go_forward():
        actions.user.joplin("historyForward")

    def find_everywhere(text: str):
        actions.user.joplin("focusSearch")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def replace(text: str):
        actions.user.joplin("showLocalSearch")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def split_window():
        actions.user.joplin("toggleVisiblePanes")

    def split_window_vertically():
        actions.user.joplin("toggleVisiblePanes")

    def split_flip():
        actions.user.joplin("toggleEditors")

    def split_clear():
        actions.user.joplin("resetLayout")

    def split_next():
        actions.user.joplin("focusElementNoteViewer")

    def split_last():
        actions.user.joplin("focusElementNoteBody")
