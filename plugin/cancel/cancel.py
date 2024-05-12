# to disable command cancellation, comment out this entire file.
# you may also wish to adjust the commands in misc/cancel.talon.

import time

from talon import Context, actions, speech_system
from talon.grammar import Phrase

# To change the phrase used to cancel commands, you must also adjust misc/cancel.talon
cancel_phrase = "cancel cancel".split()

ctx = Context()

ts_threshold: float = 0


@ctx.action_class("speech")
class SpeechActions:
    # When Talon wakes we set the timestamp threshold. On the next command we
    # will compare the phrase timestamp to the threshold and cancel any phrase
    # started before wakeup. This is to prevent commands from being executed if
    # the user wakes Talon using a noise or keypress
    def enable():
        global ts_threshold
        ts_threshold = time.perf_counter()
        actions.next()


def pre_phrase(phrase: Phrase):
    global ts_threshold

    # Nothing to cancel
    if "parsed" not in phrase:
        return

    # Check if the phrase is before the threshold
    if ts_threshold != 0:
        words = phrase["phrase"]
        # Start of phrase is before timestamp threshold
        start = getattr(words[0], "start", phrase["_ts"])
        delta = ts_threshold - start
        ts_threshold = 0
        if delta > 0:
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
