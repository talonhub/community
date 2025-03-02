# to disable command cancellation, comment out this entire file.
# you may also wish to adjust the commands in misc/cancel.talon.

import time

from talon import Context, Module, actions, speech_system
from talon.grammar import Phrase

# To change the phrase used to cancel commands, you must also adjust misc/cancel.talon
cancel_phrase = "cancel cancel".split()

mod = Module()
ctx = Context()

ts_threshold: float = 0


@ctx.action_class("speech")
class SpeechActions:
    # When Talon wakes we set the timestamp threshold. On the next command we
    # will compare the phrase timestamp to the threshold and cancel any phrase
    # started before wakeup. This is to prevent speech said before wake-up to
    # be interpreted as a command if the user wakes Talon using a noise or
    # keypress.
    def enable():
        actions.user.cancel_current_phrase()
        actions.next()


@mod.action_class
class Actions:
    def cancel_current_phrase():
        """Cancel/abort current spoken phrase"""
        global ts_threshold
        ts_threshold = time.perf_counter()


def pre_phrase(phrase: Phrase):
    global ts_threshold

    words = phrase["phrase"]

    if not words:
        return

    # Check if the phrase is before the threshold
    if ts_threshold != 0:
        # NB: mimic() and Dragon don't have this key.
        start = getattr(words[0], "start", None) or phrase.get("_ts", ts_threshold)
        phrase_starts_before_threshold = start < ts_threshold
        ts_threshold = 0
        # Start of phrase is before threshold timestamp
        if phrase_starts_before_threshold:
            print(f"Canceled phrase: {' '.join(words)}")
            cancel_entire_phrase(phrase)
            return

    # Check if the phrase is a cancel command
    n = len(cancel_phrase)
    before, after = words[:-n], words[-n:]
    if after == cancel_phrase:
        actions.app.notify(f"Command canceled: {' '.join(before)!r}")
        cancel_entire_phrase(phrase)
        return


def cancel_entire_phrase(phrase: Phrase):
    phrase["phrase"] = []
    if "parsed" in phrase:
        phrase["parsed"]._sequence = []


speech_system.register("pre:phrase", pre_phrase)
