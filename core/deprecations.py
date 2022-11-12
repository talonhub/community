"""
Helpers for deprecating voice commands, actions, and captures. Since Talon can
be an important part of people's workflows providing a warning before removing
functionality is encouraged.

The normal deprecation process in knausj_talon is as follows:

1. For 4 months from deprecation a deprecated action or command should
   continue working. Put an entry in the BREAKING_CHANGES.txt file in the
   project root to mark the deprecation and potentially explain how users can
   migrate. Use the user.deprecate_command, user.deprecate_action, or
   user.deprecate_capture actions to notify users.
2. After 4 months you can delete the deprecated command, action, or capture.
   Leave the note in BREAKING_CHANGES.txt so people who missed the
   notifications can see what happened.

If for some reason you can't keep the functionality working for 4 months,
just put the information in BREAKING_CHANGES.txt so people can look there to
see what happened.

Usages:

    # myfile.talon - demonstrate voice command deprecation
    ...
    old legacy command:
        user.deprecate_command("2022-11-10", "old legacy command")
        # perform command

    # myfile.py - demonstrate action deprecation
    from talon import actions

    @mod.action_class
    class Actions:
        def legacy_action():
            actions.user.deprecate_action("2022-10-01", "user.legacy_action")
            # Perform action

    # otherfile.py - demostrate capture deprecation
    @mod.capture(rule="...")
    def legacy_capture(m) -> str:
        actions.user.deprecate_capture("2023-09-03", "user.legacy_capture")
        # implement capture

See https://github.com/knausj85/knausj_talon/issues/940 for original discussion
"""

import datetime

from talon import Module, actions

mod = Module()

# Tells us the last time a notification was shown so we can
# decide when to re-show it without annoying the user too
# much
notification_last_shown = {}


@mod.action_class
class Acions:
    def deprecate_notify(id: str, message: str):
        """
        Notify the user about a deprecation/deactivation. id uniquely
        identifies this deprecation.
        """

        maybe_last_shown = notification_last_shown.get(id)
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(hours=2)
        if maybe_last_shown is not None and maybe_last_shown > threshold:
            return

        print("Deprecation warning: " + message)
        actions.app.notify(message, "Deprecation warning")
        notification_last_shown[id] = now

    def deprecate_command(time_deprecated: str, name: str):
        """
        Notify the user that the given voice command is deprecated and should
        not be used into the future.
        """

        id = f"command.{name}.{time_deprecated}"
        msg = (
            f'The "{name}" voice command was deprecated on '
            f"{time_deprecated}. See BREAKING_CHANGES.txt for details."
        )
        actions.user.deprecate_notify(id, msg)

    def deprecate_capture(time_deprecated: str, name: str):
        """
        Notify the user that the given capture is deprecated and should
        not be used into the future.
        """

        id = f"capture.{name}.{time_deprecated}"
        msg = (
            f'The "{name}" capture was deprecated on '
            f"{time_deprecated}. See BREAKING_CHANGES.txt for details."
        )
        actions.user.deprecate_notify(id, msg)

    def deprecate_action(time_deprecated: str, name: str):
        """
        Notify the user that the given action is deprecated and should
        not be used into the future.
        """

        id = f"action.{name}.{time_deprecated}"
        msg = (
            f'The "{name}" action was deprecated on '
            f"{time_deprecated}. See BREAKING_CHANGES.txt for details."
        )
        actions.user.deprecate_notify(id, msg)
