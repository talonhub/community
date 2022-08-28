
from talon import Module

mod = Module()

mod.tag(
    "command_client", desc="For applications which implement File based RPC with Talon"
)


@mod.action_class
class Actions:
    def command_server_directory() -> str:
        """The dirctory which contains the files required for communication between the application and Talon.
        This is the only function which absolutely must be implemented for any application using the command-client."""

    def emit_pre_phrase_signal() -> bool:
        """The command client can touch a signal file at the start of a phrase. If your
        implementation does not require this, override emit_pre_phrase_signal to
        return False."""
        # Unless we're in a command client app, we do nothing.
        return False
