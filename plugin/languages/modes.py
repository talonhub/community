from typing import Union

from talon import Module, actions, cron
from talon.grammar import Phrase

mod = Module()


@mod.action_class
class Actions:
    def command_mode(phrase: Union[Phrase, str] = None):
        """Enter command mode and re-evaluate phrase"""
        # I checked and I couldn't find a method to get the current mode. so as a hack we are disabling all possible modes.
        print("Entering command mode")
        actions.mode.disable("user.whisper")

        actions.mode.enable("command")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def whisper_mode():
        """Enter whisper mode"""
        print("Entering whisper mode")
        actions.mode.disable("command")
        actions.mode.enable("user.whisper")
