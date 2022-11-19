"""
Helpers for deprecating voice commands, actions, and captures. Since Talon can
be an important part of people's workflows providing a warning before removing
functionality is encouraged.

The normal deprecation process in knausj_talon is as follows:

1. For 6 months from deprecation a deprecated action or command should
   continue working. Put an entry in the BREAKING_CHANGES.txt file in the
   project root to mark the deprecation and potentially explain how users can
   migrate. Use the user.deprecate_command, user.deprecate_action, or
   user.deprecate_capture actions to notify users.
2. After 6 months you can delete the deprecated command, action, or capture.
   Leave the note in BREAKING_CHANGES.txt so people who missed the
   notifications can see what happened.

If for some reason you can't keep the functionality working for 6 months,
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
import warnings
import os.path

from talon import Module, actions, speech_system

REPO_DIR = os.path.dirname(os.path.dirname(__file__))

mod = Module()
setting_deprecation_warning_interval_hours = mod.setting(
    "deprecation_warning_interval_hours",
    type=float,
    desc="""How long, in hours, to wait before notifying the user again of a
    deprecated action/command/capture.""",
    default=24,
)

# Tells us the last time a notification was shown so we can
# decide when to re-show it without annoying the user too
# much
notification_last_shown = {}

# This gets reset on every phrase, so we avoid notifying more than once per
# phrase.
notified_in_phrase = set()
def post_phrase(_ignored):
    global notified_in_phrase
    notified_in_phrase = set()
speech_system.register("post:phrase", post_phrase)


@mod.action_class
class Actions:
    def deprecate_notify(id: str, message: str):
        """
        Notify the user about a deprecation/deactivation. id uniquely
        identifies this deprecation.
        """

        maybe_last_shown = notification_last_shown.get(id)
        now = datetime.datetime.now()
        interval = setting_deprecation_warning_interval_hours.get()
        threshold = now - datetime.timedelta(hours=interval)
        if maybe_last_shown is not None and maybe_last_shown > threshold:
            return

        print("Deprecation warning: " + message)
        actions.app.notify(message, "Deprecation warning")
        notification_last_shown[id] = now

    def deprecate_command(time_deprecated: str, name: str, replacement: str):
        """
        Notify the user that the given voice command is deprecated and should
        not be used into the future; the command `replacement` should be used
        instead.
        """

        if name in notified_in_phrase: return
        notified_in_phrase.add(name)
        msg = (
            f'The "{name}" command is deprecated. Instead, say: "{replacement}".'
            f' See log for more.'
        )
        actions.app.notify(msg, "Deprecation warning")
        msg = (
            f'The "{name}" command is deprecated since {time_deprecated}.'
            f' Instead, say: "{replacement}".'
            f' See {os.path.join(REPO_DIR, "BREAKING_CHANGES.txt")}'
        )
        warnings.warn(msg, DeprecationWarning)

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
