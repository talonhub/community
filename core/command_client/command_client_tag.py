from talon import Module

mod = Module()

mod.tag(
    "command_client", desc="For applications which implement file-based RPC with Talon"
)


@mod.action_class
class Actions:
    def command_server_directory() -> str:
        """
        The dirctory which contains the files required for communication between
        the application and Talon. This is the only function which absolutely
        must be implemented for any application using the command-client.  Each
        application that supports file-based RPC should use its own directory
        name.  Note that this action should only return a name; the parent
        directory is determined by the core command client code.
        """
