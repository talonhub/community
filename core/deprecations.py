"""
Helpers for deprecating voice commands, actions, and captures. Since Talon can
be an important part of people's workflows providing a warning before removing
functionality is encouraged.

The normal deprecation process in `community` is as follows:

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
        # This will show a notification to say use 'new command' instead of
        # 'old legacy command'. No removal of functionality is allowed.
        user.deprecate_command("2022-11-10", "old legacy command", "new command")
        # perform command

    new command:
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

See https://github.com/talonhub/community/issues/940 for original discussion
"""

import datetime
import os.path
import warnings

from talon import Module, actions, settings, speech_system

REPO_DIR = os.path.dirname(os.path.dirname(__file__))

mod = Module()
mod.setting(
    "deprecate_warning_interval_hours",
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


def calculate_rule_info():
    """
    Try to work out the .talon file and line of the command that is executing
    """
    try:
        current_command = actions.core.current_command__unstable()
        start_line = current_command[0].target.start_line
        filename = current_command[0].target.filename
        rule = " ".join(current_command[1]._unmapped)
        return f'\nTriggered from "{rule}" ({filename}:{start_line})'
    except Exception as e:
        return ""


def deprecate_notify(id: str, message: str):
    """
    Notify the user about a deprecation/deactivation. id uniquely
    identifies this deprecation.
    """

    maybe_last_shown = notification_last_shown.get(id)
    now = datetime.datetime.now()
    interval = settings.get("user.deprecate_warning_interval_hours")
    threshold = now - datetime.timedelta(hours=interval)
    if maybe_last_shown is not None and maybe_last_shown > threshold:
        return

    actions.app.notify(message, "Deprecation warning")
    notification_last_shown[id] = now


def post_phrase(_ignored):
    global notified_in_phrase
    notified_in_phrase = set()


speech_system.register("post:phrase", post_phrase)


@mod.action_class
class Actions:
    def deprecate_command(time_deprecated: str, name: str, replacement: str):
        """
        Notify the user that the given voice command is deprecated and should
        not be used into the future; the command `replacement` should be used
        instead.
        """

        if name in notified_in_phrase:
            return

        # Want to tell users every time they use a deprecated command since
        # they should immediately be retraining to use {replacement}. Also
        # so if they repeat the command they get another chance to read
        # the popup message.
        notified_in_phrase.add(name)
        msg = (
            f'The "{name}" command is deprecated. Instead, say: "{replacement}".'
            f" See log for more."
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

        deprecate_notify(id, f"The `{name}` capture is deprecated. See log for more.")

        msg = (
            f"The `{name}` capture is deprecated since {time_deprecated}."
            f' See {os.path.join(REPO_DIR, "BREAKING_CHANGES.txt")}'
            f"{calculate_rule_info()}"
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=3)

    def deprecate_action(time_deprecated: str, name: str):
        """
        Notify the user that the given action is deprecated and should
        not be used into the future.
        """

        id = f"action.{name}.{time_deprecated}"

        deprecate_notify(id, f"The `{name}` action is deprecated. See log for more.")

        msg = (
            f"The `{name}` action is deprecated since {time_deprecated}."
            f' See {os.path.join(REPO_DIR, "BREAKING_CHANGES.txt")}'
            f"{calculate_rule_info()}"
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=5)
