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

    # Nothing to cancel
    if not phrase.get("phrase") or "parsed" not in phrase:
        return

    # Check if the phrase is before the threshold
    if ts_threshold != 0:
        words = phrase["phrase"]
        start = getattr(words[0], "start", phrase["_ts"])
        phrase_starts_before_threshold = start < ts_threshold
        ts_threshold = 0
        # Start of phrase is before threshold timestamp
        if phrase_starts_before_threshold:
            abort_phrase(phrase)
            return

    # Check if the phrase is a cancel command
    if "text" in phrase:
        n = len(cancel_phrase)
        before, after = phrase["text"][:-n], phrase["text"][-n:]
        if after == cancel_phrase:
            actions.app.notify(f"Command canceled: {' '.join(before)!r}")
            abort_phrase(phrase)
            return


def abort_phrase(phrase: Phrase):
    phrase["parsed"]._sequence = []


speech_system.register("pre:phrase", pre_phrase)
