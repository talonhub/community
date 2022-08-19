import string

from talon import Module

mod = Module()

mod.tag(
    "command_client", desc="For applications which implement File based RPC with Talon"
)


@mod.action_class
class Actions:
    def command_server_directory() -> string:
        """The dirctory which contains the files required for communication between the application and Talon.
        This is the only function which absolutly must be implemented for any application using the command-client."""

    def emit_pre_phrase_signal() -> bool:
        """The command client can touch a signal file at the start of a phrase, function has a default implementation
        which does this, if your implementation does not require this signal file be touched simply return false."""

    def command_client_fallback(command_id: str):
        """Execute an alternative stratagy for issuing the command, if non exists just implemnt
        there is not need to implement, the fall back is to do nothing."""
