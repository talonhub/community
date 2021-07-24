from talon import Module, actions, cron
from talon.grammar import Phrase
from typing import Union

mod = Module()


@mod.action_class
class Actions:
    def text_field_mode(phrase: Union[Phrase, str] = None):
        """Enter dictation mode and re-evaluate phrase"""
        # We should get the current mode instead of the "command" mode here.
        actions.mode.disable("command")
        actions.mode.enable("user.text_field")

        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def command_mode(phrase: Union[Phrase, str] = None):
        """Enter command mode and re-evaluate phrase"""
        # I checked and I couldn't find a method to get the current mode. so as a hack we are disabling all possible modes.
        actions.mode.disable("dictation")
        actions.mode.disable("user.polish_dictation")
        actions.mode.disable("user.text_field")

        actions.mode.enable("command")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def dictation_mode(phrase: Union[Phrase, str] = None):
        """Enter dictation mode and re-evaluate phrase"""
        actions.mode.disable("command")
        actions.mode.enable("dictation")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def polish_dictation_mode(phrase: Union[Phrase, str] = None):
        """Enter dictation mode and re-evaluate phrase"""
        actions.mode.disable("command")
        actions.mode.enable("user.polish_dictation")
        if phrase:
            actions.user.rephrase(phrase, run_async=False)
