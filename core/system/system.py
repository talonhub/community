from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def system_switch_screen_power(on: bool):
        """Turns all screens off or on."""

    def system_show_settings():
        """Shows the system settings."""

    def system_show_task_manager():
        """Starts the system's task manager app or reshows its window."""

    def system_lock():
        """Locks the system, requiring a password or similar means to unlock it."""

    def system_show_exit_menu():
        """Shows the system's exit menu or dialog, including options for shutting down and restarting, among others."""
